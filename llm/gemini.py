from django.conf import settings
from django.core.exceptions import ValidationError
from google import genai
from google.genai import types
from pydantic import BaseModel

from llm.taxonomies import SummaryLength

client = genai.Client(api_key=settings.GEMINI_API_KEY)


def get_output_token(
    summary_length: SummaryLength = SummaryLength.SHORT,
) -> int:
    return {
        SummaryLength.SHORT: 120,
        SummaryLength.MEDIUM: 240,
        SummaryLength.LONG: 360,
    }.get(summary_length)


class GeminiResponseSchema(BaseModel):
    title: str
    summary: str


def get_summary_from_google(
    content: str, summary_length: SummaryLength = SummaryLength.SHORT
) -> GeminiResponseSchema:
    try:
        generate_content_config = types.GenerateContentConfig(
            temperature=0.1,
            max_output_tokens=2560,
            response_mime_type="application/json",
            response_schema=GeminiResponseSchema,
        )

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                f"Write a summary in {get_output_token(summary_length)} words",
                content,
            ],
            config=generate_content_config,
        )

        if response.parsed:
            return response.parsed
        if response.text:
            return GeminiResponseSchema.model_validate_json(response.text)
    except genai.errors.ClientError as e:
        raise ValidationError(e.message, code="invalid")
    except Exception as e:
        raise e
