import io
import json
from typing import BinaryIO
import pdfplumber

from src.core import prompts
from src.core.agent import agent
from src.exceptions.PdfExtractException import PdfExtractException


def _read_pdf_file(file: io.BytesIO | BinaryIO) -> str:
    """Извлекает текст из PDF"""
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


async def extract_metrics_from_pdf(file: io.BytesIO | BinaryIO) -> str:
    """Извлекает текст из PDF файла"""
    try:
        return _read_pdf_file(file)
    except Exception as e:
        raise PdfExtractException(detail=str(e))