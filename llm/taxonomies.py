# Standard Library
from typing import Any, Dict, List

from django.db.models import TextChoices


def serialize(klass) -> List[Dict[str, Any]]:
    return [
        {"name": x[1], "value": x[0]} for x in getattr(klass, "choices", [])
    ]


class SummaryLength(TextChoices):
    """
    Choices for summary length, helps in setting the output length of summary
    """

    SHORT = "SHORT", "Short"
    MEDIUM = "MEDIUM", "Medium"
    LONG = "LONG", "Long"
