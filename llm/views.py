from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from llm.forms import SummaryForm
from llm.models import Summary


class HomePageView(FormView):
    form_class = SummaryForm
    template_name = "llm/home.html"
    success_url = reverse_lazy("llm:history")

    def form_valid(self, form: SummaryForm):
        form.save()
        return redirect(self.success_url)


class HistoryPageView(TemplateView):
    template_name = "llm/history.html"

    def get_context_data(self, **kwargs):
        ctx = super(HistoryPageView, self).get_context_data(**kwargs)
        ctx["history"] = Summary.objects.all()
        return ctx


class SummaryPageView(TemplateView):
    template_name = "llm/summary.html"

    def get_context_data(self, summary_uid, **kwargs):
        ctx = super(SummaryPageView, self).get_context_data(**kwargs)
        ctx["summary"] = get_object_or_404(Summary, uid=summary_uid)
        return ctx
