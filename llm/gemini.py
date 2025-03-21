from django.conf import settings
from google import genai
from google.genai import types
from pydantic import BaseModel

client = genai.Client(api_key=settings.GEMINI_API_KEY)


class GeminiResponseSchema(BaseModel):
    title: str
    summary: str


def get_summary_from_google(content: str):
    generate_content_config = types.GenerateContentConfig(
        temperature=0.1,
        max_output_tokens=256,
        response_mime_type="application/json",
        response_schema=GeminiResponseSchema,
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[content],
        config=generate_content_config,
    )
    return response.parsed
