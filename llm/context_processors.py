# App Imports
from llm.taxonomies import SummaryLength, serialize


def default_website_data(request) -> dict:
    """
    Send context data django template, could be used for static
    data for all users
    """
    return dict(choices=dict(summary_length=serialize(SummaryLength)))
