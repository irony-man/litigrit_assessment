# Standard Library

# App Imports
from rest_framework import serializers

from llm.models import Summary


class SummarySerializer(serializers.ModelSerializer):
    """
    Serializer for Summary model which has read only
    fields, means these fields cannot be edited from
    frontend form data.
    """

    class Meta:
        model = Summary
        fields = [
            "uid",
            "attachment",
            "summary_length",
            "extracted_text",
            "title",
            "summary",
            "session_uid",
        ]
        read_only_fields = [
            "uid",
            "extracted_text",
            "title",
            "summary",
        ]
