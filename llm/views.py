from django.contrib.auth import authenticate, login, logout
from django.db.models import Case, F, TextField, Value, When
from django.db.models.functions import Concat, Length, Substr
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from llm.forms import LoginForm, SignupForm, SummaryForm
from llm.mixins import AuthMixin
from llm.models import Summary


def is_ajax(request) -> bool:
    return request.headers.get("x-requested-with") == "XMLHttpRequest"


class LoginPageView(FormView):
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
        return redirect(self.success_url)


class SignupPageView(FormView):
    form_class = SignupForm
    template_name = "llm/signup.html"
    success_url = reverse_lazy("llm:home")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super(SignupPageView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form: SignupForm):
        login(self.request, form.cleaned_data["user"])
        return redirect(self.success_url)


class LogoutView(AuthMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse_lazy("llm:home"))


class HomePageView(TemplateView):
    template_name = "llm/home.html"

    def get_context_data(self, **kwargs):
        ctx = super(HomePageView, self).get_context_data(**kwargs)
        ctx["history"] = (
            Summary.objects.annotate(
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


class SummaryFormView(FormView):
    form_class = SummaryForm
    template_name = "llm/home.html"
    success_url = reverse_lazy("llm:home")

    def form_valid(self, form: SummaryForm):
        Summary.objects.create(**form.cleaned_data)
        if is_ajax(self.request):
            return JsonResponse(
                data={
                    "message": "Summary Created",
                    "success_url": self.success_url,
                },
                status=201,
            )
        return redirect(self.success_url)

    def form_invalid(self, form: SummaryForm):
        if is_ajax(self.request):
            return JsonResponse(
                {
                    "errors": dict(form.errors.items()),
                },
                status=400,
            )
        return super(SummaryFormView, self).form_invalid(form)


class SummaryPageView(TemplateView):
    template_name = "llm/summary.html"

    def get_context_data(self, uid, **kwargs):
        ctx = super(SummaryPageView, self).get_context_data(**kwargs)
        ctx["summary"] = get_object_or_404(Summary, uid=uid)
        return ctx
