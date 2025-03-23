# App Imports
from django.forms import ModelForm

from llm.gemini import GeminiResponseSchema, get_summary_from_google
from llm.models import Summary
from llm.utils import extract_text_from_pdf


class SummaryForm(ModelForm):
    class Meta:
        model = Summary
        fields = ("attachment", "summary_length")

    def clean(self):
        cleaned_data = self.cleaned_data
        cleaned_data["extracted_text"] = extract_text_from_pdf(
            cleaned_data.get("attachment")
        )

        gemini_response: GeminiResponseSchema = get_summary_from_google(
            cleaned_data["extracted_text"], cleaned_data.get("summary_length")
        )
        cleaned_data["title"] = gemini_response.title
        cleaned_data["summary"] = gemini_response.summary
        return cleaned_data
