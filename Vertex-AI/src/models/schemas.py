from __future__ import annotations

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional


class FinanceMetric(BaseModel):
    name: str = Field(description="Человекочитаемое имя показателя")
    value: float = Field(description="Числовое значение показателя")
    unit: str = Field(description="Единицы измерения")
    year: Optional[int] = Field(default=None, description="Год показателя")
    confidence_score: float = Field(ge=0.0, le=1.0, description="Оценка уверенности (0–1)")
    source_fragment: str = Field(description="Фрагмент текста источника")

    @field_validator('confidence_score')
    @classmethod
    def validate_confidence(cls, v: float) -> float:
        return round(v, 2)


class FinanceRatio(BaseModel):
    name: str = Field(description="Название коэффициента")
    value: Optional[float] = Field(default=None, description="Значение коэффициента")
    unit: str = Field(description="Единицы измерения")
    year: Optional[int] = Field(default=None, description="Год коэффициента")
    formula: str = Field(description="Формула коэффициента")
    category: Optional[str] = Field(default=None, description="Категория")


class AnalyzeResponse(BaseModel):
    raw_text: str = Field(description="Сырой текст из PDF")
    warnings: List[str] = Field(default_factory=list, description="Предупреждения")
    metrics: List[FinanceMetric] = Field(description="Финансовые показатели")
    ratios: List[FinanceRatio] = Field(description="Финансовые коэффициенты")
    score: Optional[float] = Field(default=None, description="Интегральный скоринг (0-100)")
    nlp_summary: Optional[str] = Field(default=None, description="Резюме NLP")
    risks: List[str] = Field(default_factory=list, description="Риски")
    opportunities: List[str] = Field(default_factory=list, description="Возможности")
    recommendations: List[str] = Field(default_factory=list, description="Рекомендации")
    news: List[str] = Field(default_factory=list, description="Новости")