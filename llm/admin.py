from django.contrib import admin

from llm.models import Summary


@admin.register(Summary)
class SummaryAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "summary",
        "attachment",
        "created",
        "updated",
    )
    readonly_fields = (
        "title",
        "summary",
        "extracted_text",
        "created",
        "updated",
    )
