import pymupdf


def extract_text_from_pdf(pdf):
    doc = pymupdf.open(pdf)
    return "\n".join(page.get_text().strip() for page in doc)
