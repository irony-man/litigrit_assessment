from django.db.models import Case, F, TextField, Value, When
from django.db.models.functions import Concat, Length, Substr
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from llm.forms import SummaryForm
from llm.models import Summary


class HomePageView(FormView):
    form_class = SummaryForm
    template_name = "llm/home.html"
    success_url = reverse_lazy("llm:home")

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

    def form_valid(self, form: SummaryForm):
        if attachment := form.cleaned_data.get("attachment"):
            Summary.objects.create(attachment=attachment)
        return redirect(self.success_url)


class SummaryPageView(TemplateView):
    template_name = "llm/summary.html"

    def get_context_data(self, summary_uid, **kwargs):
        ctx = super(SummaryPageView, self).get_context_data(**kwargs)
        ctx["summary"] = get_object_or_404(Summary, uid=summary_uid)
        return ctx
