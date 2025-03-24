import uuid

from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.db.models import Case, F, TextField, Value, When
from django.db.models.functions import Concat, Length, Substr
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from rest_framework.exceptions import (
    APIException,
)
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.status import (
    HTTP_200_OK,
)
from rest_framework.views import APIView

from llm.forms import LoginForm, SignupForm
from llm.gemini import GeminiResponseSchema, get_summary_from_google
from llm.mixins import AuthMixin
from llm.models import Summary
from llm.serializers import SummarySerializer
from llm.utils import extract_text_from_pdf


def is_ajax(request) -> bool:
    return request.headers.get("x-requested-with") == "XMLHttpRequest"


class LoginPageView(FormView):
    """
    Form View to log in the user, this uses django template
    """

    form_class = LoginForm
    template_name = "llm/login.html"
    success_url = reverse_lazy("llm:home")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super(LoginPageView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form: LoginForm):
        user = authenticate(
            self.request,
            username=form.cleaned_data.get("username"),
            password=form.cleaned_data.get("password"),
        )
        if not user:
            form.errors.password = ("Invalid login credentials!!",)
            return super(LoginPageView, self).form_invalid(form)
        login(self.request, user)
        self.request.session["uid"] = None
        return redirect(self.success_url)


class SignupPageView(FormView):
    """
    Form View to sign up the user
    """

    form_class = SignupForm
    template_name = "llm/signup.html"
    success_url = reverse_lazy("llm:home")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super(SignupPageView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form: SignupForm):
        login(self.request, form.cleaned_data["user"])
        self.request.session["uid"] = None
        return redirect(self.success_url)


class LogoutView(AuthMixin, TemplateView):
    """
    View to logout the user if logged in
    """

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse_lazy("llm:home"))


class HomePageView(TemplateView):
    template_name = "llm/home.html"

    def get_context_data(self, **kwargs):
        """
        Fetches chat history based on user's login status.

        Reduces the extracted text length to 300 for optimized
        list view using django ORM's annotate
        """
        ctx = super(HomePageView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            filters = dict(user__id=self.request.user.id)
        elif uid := self.request.session.get("uid"):
            filters = dict(session_uid=uid)
        else:
            filters = dict(uid=None)
        ctx["history"] = (
            Summary.objects.filter(**filters)
            .annotate(
                extracted_text_length=Length("extracted_text"),
                short_extracted_text=Case(
                    When(
                        extracted_text_length__gt=300,
                        then=Concat(
                            Substr("extracted_text", 1, 300), Value("...")
                        ),
                    ),
                    default=F("extracted_text"),
                    output_field=TextField(),
                ),
            )
            .values(
                "uid",
                "created",
                "title",
                "summary",
                "short_extracted_text",
                "attachment",
            )
            .order_by("created")
        )
        return ctx


class SummaryAPIView(APIView):
    """
    Summary post using DRF, we can also use FormView but I wanted to showcase
    DRF skills. It assign values to Summary instance which we fetch data
    from gemini and populates user and session_uid.
    """

    def post(self, request, *args, **kwargs):
        try:
            serializer = SummarySerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance: Summary = serializer.save()

            instance.extracted_text = extract_text_from_pdf(
                instance.attachment.path
            )

            gemini_response: GeminiResponseSchema = get_summary_from_google(
                instance.extracted_text, instance.summary_length
            )
            instance.title = gemini_response.title
            instance.summary = gemini_response.summary
            if request.user.is_authenticated:
                instance.user = request.user
            else:
                uid = self.request.session.get("uid", str(uuid.uuid4()))
                self.request.session["uid"] = uid
                instance.session_uid = uid
            instance.save()

            return JsonResponse(
                SummarySerializer(instance=instance).data, status=HTTP_200_OK
            )
        except ValidationError as e:
            raise DRFValidationError(dict(detail=e))
        except DRFValidationError as e:
            raise e
        except Exception as e:
            raise APIException(e)


class SummaryPageView(TemplateView):
    """
    Sends context data to django template based on uid
    """

    template_name = "llm/summary.html"

    def get_context_data(self, uid, **kwargs):
        ctx = super(SummaryPageView, self).get_context_data(**kwargs)
        ctx["summary"] = get_object_or_404(Summary, uid=uid)
        return ctx
