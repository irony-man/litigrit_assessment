import uuid
from pathlib import Path

from django.core.exceptions import ValidationError
from django.db.models import (
    CharField,
    DateTimeField,
    FileField,
    Model,
    TextField,
    UUIDField,
)

from llm.gemini import GeminiResponseSchema, get_summary_from_google
from llm.taxonomies import SummaryLength
from llm.utils import extract_text_from_pdf


class CreateUpdate(Model):
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Summary(CreateUpdate):
    uid = UUIDField(primary_key=True, default=uuid.uuid4)
    extracted_text = TextField()
    attachment = FileField()
    title = CharField(max_length=255)
    summary = TextField()
    summary_length = CharField(
        choices=SummaryLength.choices, default=SummaryLength.SHORT
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Summaries"

    def clean(self):
        extension = Path(self.attachment.name).suffix[1:].lower()
        if extension != "pdf":
            raise ValidationError(
                {"attachment": f"File extension {extension} is not allowed. "}
            )

        self.extracted_text = extract_text_from_pdf(self.attachment)

        gemini_response: GeminiResponseSchema = get_summary_from_google(
            self.extracted_text, self.summary_length
        )
        self.title = gemini_response.title
        self.summary = gemini_response.summary
        return self
