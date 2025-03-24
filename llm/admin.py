from django.contrib import admin

from llm.models import Summary


@admin.register(Summary)
class SummaryAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "attachment",
        "summary_length",
        "user",
        "summary",
    )
    readonly_fields = (
        "title",
        "summary",
        "extracted_text",
        "created",
        "updated",
    )
