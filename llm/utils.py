import pymupdf


def extract_text_from_pdf(pdf):
    """
    Extracts the text from pdf using a library
    """
    doc = pymupdf.open(pdf)
    return "\n".join(page.get_text().strip() for page in doc)
