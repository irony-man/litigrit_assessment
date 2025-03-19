from tika import parser


def extract_text_from_pdf(pdf_path):
    raw = parser.from_file(pdf_path)
    return raw["content"].strip()
