import io
import json
from typing import BinaryIO

from src.core.ratios import calculate_ratios
from src.core.scoring import calculate_score
from src.core.nlp import analyze_risks_and_opportunities
from src.core.recommendations import generate_recommendations
from src.exceptions.PdfExtractException import PdfExtractException
from src.models.schemas import FinanceMetric
from src.core.agent import agent
from src.core import prompts


def _read_pdf_file(file: io.BytesIO | BinaryIO) -> str:
    """Извлекает текст из PDF"""
    import pdfplumber
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


async def analyze_pdf(file: io.BytesIO | BinaryIO):
    warnings = []

    try:
        raw_text = _read_pdf_file(file)

        if not raw_text or len(raw_text.strip()) < 100:
            warnings.append("PDF содержит мало текста. Возможно, это скан без OCR.")

        print("🤖 Request to AI for metrics extraction...")

        prompt = f"""
Извлеки финансовые метрики из текста отчета. Верни ТОЛЬКО валидный JSON массив.

Текст отчета:
{raw_text[:8000]}
"""

        res = await agent.request(
            "vertex-analysis-chat",
            prompt,
            system=prompts.PDF_EXTRACT_METRICS
        )

        metrics = []
        if res and "content" in res:
            try:
                content = res["content"]
                start_idx = content.find("[")
                end_idx = content.rfind("]") + 1
                if start_idx != -1 and end_idx != -1:
                    json_str = content[start_idx:end_idx]
                    metrics_data = json.loads(json_str)
                    metrics = [FinanceMetric(**m) for m in metrics_data]
            except json.JSONDecodeError as e:
                warnings.append(f"Ошибка парсинга JSON от AI: {e}")

        ratios = calculate_ratios(metrics)
        score = calculate_score(ratios)

        print("🧠 Running NLP analysis...")
        nlp_data = await analyze_risks_and_opportunities(raw_text)

        recommendations = generate_recommendations(metrics, ratios, score, nlp_data)

        return {
            "raw_text": raw_text[:2000] + "..." if len(raw_text) > 2000 else raw_text,
            "warnings": warnings,
            "metrics": [m.model_dump() for m in metrics],
            "ratios": [r.model_dump() for r in ratios],
            "score": score,
            "nlp_summary": nlp_data.get("summary"),
            "risks": nlp_data.get("risks", []),
            "opportunities": nlp_data.get("opportunities", []),
            "recommendations": recommendations,
            "news": []
        }

    except Exception as e:
        raise PdfExtractException(detail=str(e))