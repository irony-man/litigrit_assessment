from django.db.models.signals import post_save
from django.dispatch import receiver

from llm.gemini import GeminiResponseSchema, get_summary_from_google
from llm.models import Summary
from llm.utils import extract_text_from_pdf


@receiver(post_save, sender=Summary)
def on_summary_save(sender, instance: Summary, **kwargs):
    if not instance.extracted_text:
        instance.extracted_text = extract_text_from_pdf(
            instance.attachment.path
        )

        gemini_response: GeminiResponseSchema = get_summary_from_google(
            instance.extracted_text
        )
        instance.title = gemini_response.title
        instance.summary = gemini_response.summary
        instance.save()
