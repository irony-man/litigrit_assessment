# App Imports
from django.forms import ModelForm

from llm.models import Summary


class SummaryForm(ModelForm):
    class Meta:
        model = Summary
        fields = ("attachment",)
