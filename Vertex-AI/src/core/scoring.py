from typing import List
from src.models.schemas import FinanceRatio


def calculate_score(ratios: List[FinanceRatio]) -> float | None:
    """Рассчитывает интегральный скоринг компании (0-100)"""
    if not ratios:
        return None

    scored_ratios = []

    for ratio in ratios:
        if ratio.value is None:
            continue

        score = 0.0

        if ratio.category == "Ликвидность":
            if ratio.name == "Коэффициент текущей ликвидности":
                if 1.5 <= ratio.value <= 2.5:
                    score = 1.0
                elif 1.0 <= ratio.value < 1.5:
                    score = 0.7
                elif ratio.value > 2.5:
                    score = 0.6
                else:
                    score = 0.3

        elif ratio.category == "Рентабельность":
            if ratio.value >= 0.20:
                score = 1.0
            elif ratio.value >= 0.10:
                score = 0.8
            elif ratio.value >= 0.05:
                score = 0.6
            elif ratio.value >= 0:
                score = 0.4
            else:
                score = 0.2

        elif ratio.category == "Финансовая устойчивость":
            if "Доля собственного капитала" in ratio.name:
                if ratio.value >= 0.5:
                    score = 1.0
                elif ratio.value >= 0.3:
                    score = 0.7
                else:
                    score = 0.4
            elif "левериджа" in ratio.name.lower():
                if ratio.value <= 1.0:
                    score = 1.0
                elif ratio.value <= 2.0:
                    score = 0.7
                elif ratio.value <= 3.0:
                    score = 0.5
                else:
                    score = 0.3

        elif ratio.category == "Деловая активность":
            if ratio.value >= 1.5:
                score = 1.0
            elif ratio.value >= 1.0:
                score = 0.8
            elif ratio.value >= 0.5:
                score = 0.6
            else:
                score = 0.4

        scored_ratios.append(score)

    if not scored_ratios:
        return None

    return round(sum(scored_ratios) / len(scored_ratios) * 100, 1)