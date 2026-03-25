from typing import List, Dict, Any
from src.models.schemas import FinanceRatio, FinanceMetric


def generate_recommendations(
        metrics: List[FinanceMetric],
        ratios: List[FinanceRatio],
        score: float | None,
        nlp_data: Dict[str, Any]
) -> List[str]:
    """Генерирует рекомендации на основе анализа"""
    recommendations = []

    for ratio in ratios:
        if ratio.value is None:
            continue

        if ratio.category == "Ликвидность":
            if ratio.value < 1.0:
                recommendations.append(
                    "🔴 КРИТИЧНО: Коэффициент ликвидности ниже 1.0. "
                    "Рекомендуется срочно увеличить оборотные активы."
                )
            elif ratio.value < 1.5:
                recommendations.append(
                    "⚠️ Коэффициент ликвидности ниже оптимального. "
                    "Рассмотрите улучшение управления оборотным капиталом."
                )

        elif ratio.category == "Рентабельность":
            if ratio.value < 0:
                recommendations.append(
                    f"🔴 Отрицательная {ratio.name}. "
                    "Необходим срочный анализ причин убыточности."
                )
            elif ratio.value < 0.05:
                recommendations.append(
                    f"⚠️ Низкая {ratio.name} (менее 5%). "
                    "Рекомендуется анализ структуры затрат."
                )

        elif ratio.category == "Финансовая устойчивость":
            if "левериджа" in ratio.name.lower() and ratio.value > 2.0:
                recommendations.append(
                    "⚠️ Высокая долговая нагрузка. "
                    "Рассмотрите снижение заемного финансирования."
                )

    if score is not None:
        if score < 40:
            recommendations.append(
                "🔴 Общий финансовый рейтинг низкий. "
                "Требуется комплексный антикризисный план."
            )
        elif score < 70:
            recommendations.append(
                "⚠️ Финансовое состояние удовлетворительное, "
                "но есть зоны для улучшения."
            )
        else:
            recommendations.append(
                "✅ Компания демонстрирует хорошие финансовые показатели."
            )

    if nlp_data.get("risks"):
        recommendations.append(
            f"📋 Выявлено рисков: {len(nlp_data['risks'])}. "
            "Рекомендуется план управления рисками."
        )

    if len(recommendations) < 2:
        recommendations.append(
            "📊 Рекомендуется регулярный мониторинг финансовых показателей."
        )

    return recommendations