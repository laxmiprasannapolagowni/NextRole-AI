from io import BytesIO

from docx import Document
from pypdf import PdfReader


def extract_text_from_pdf(file_bytes):
    """
    Extract text from a PDF resume.
    """

    pdf_file = BytesIO(file_bytes)
    reader = PdfReader(pdf_file)

    extracted_pages = []

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            extracted_pages.append(page_text)

    return "\n".join(extracted_pages)


def extract_text_from_docx(file_bytes):
    """
    Extract text from a DOCX resume.
    """

    docx_file = BytesIO(file_bytes)
    document = Document(docx_file)

    paragraphs = []

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    return "\n".join(paragraphs)


def extract_text_from_txt(file_bytes):
    """
    Extract text from a TXT resume.
    """

    return file_bytes.decode(
        "utf-8",
        errors="ignore"
    )


def extract_resume_text(uploaded_file):
    """
    Detect the uploaded resume format and extract its text.
    """

    if uploaded_file is None:
        return ""

    file_name = uploaded_file.name.lower()
    file_bytes = uploaded_file.getvalue()

    if file_name.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)

    if file_name.endswith(".docx"):
        return extract_text_from_docx(file_bytes)

    if file_name.endswith(".txt"):
        return extract_text_from_txt(file_bytes)

    raise ValueError(
        "Unsupported file type. Upload a PDF, DOCX or TXT file."
    )