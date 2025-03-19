import uuid

from django.db.models import (
    CharField,
    DateTimeField,
    FileField,
    Model,
    TextField,
    UUIDField,
)

from llm.gemini import GeminiResponseSchema, get_summary_from_google
from llm.utils import extract_text_from_pdf


class CreateUpdate(Model):
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Summary(CreateUpdate):
    uid = UUIDField(primary_key=True, default=uuid.uuid4)
    extracted_text = TextField()
    attachment = FileField(upload_to="attachments/")
    title = CharField(max_length=255)
    summary = TextField()

    def __str__(self):
        return self.attachment.name

    class Meta:
        verbose_name_plural = "Summaries"

    def save(self, *args, **kwargs):
        self.extracted_text = extract_text_from_pdf(self.attachment.name)
        gemini_response: GeminiResponseSchema = get_summary_from_google(
            self.extracted_text
        )
        self.title = gemini_response.title
        self.summary = gemini_response.summary
        return super(Summary, self).save(*args, **kwargs)
