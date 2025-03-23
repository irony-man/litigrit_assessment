# App Imports
from llm.taxonomies import SummaryLength, serialize


def default_website_data(request) -> dict:
    return dict(choices=dict(summary_length=serialize(SummaryLength)))
