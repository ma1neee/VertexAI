from typing import List
from src.models.schemas import FinanceMetric, FinanceRatio


def calculate_ratios(metrics: List[FinanceMetric]) -> List[FinanceRatio]:
    """Рассчитывает финансовые коэффициенты на основе извлеченных метрик"""
    ratios = []
    m_dict = {m.name.lower(): m for m in metrics}

    def get_metric(name_variants: List[str]) -> float | None:
        for name in name_variants:
            if name.lower() in m_dict:
                return m_dict[name.lower()].value
        return None

    def safe_div(num: float | None, denom: float | None) -> float | None:
        if num is None or denom is None or denom == 0:
            return None
        return round(num / denom, 4)

    # ЛИКВИДНОСТЬ
    current_assets = get_metric(["Оборотные активы", "Current Assets"])
    current_liabilities = get_metric(["Краткосрочные обязательства", "Current Liabilities"])

    if current_assets and current_liabilities:
        ratios.append(FinanceRatio(
            name="Коэффициент текущей ликвидности",
            value=safe_div(current_assets, current_liabilities),
            unit="x",
            year=None,
            formula="Оборотные активы / Краткосрочные обязательства",
            category="Ликвидность"
        ))

    # ФИНАНСОВАЯ УСТОЙЧИВОСТЬ
    equity = get_metric(["Собственный капитал", "Equity", "Capital"])
    total_assets = get_metric(["Активы", "Total Assets", "Assets"])
    total_liabilities = get_metric(["Обязательства", "Total Liabilities", "Liabilities"])

    if equity and total_assets:
        ratios.append(FinanceRatio(
            name="Доля собственного капитала",
            value=safe_div(equity, total_assets),
            unit="%",
            year=None,
            formula="Собственный капитал / Активы",
            category="Финансовая устойчивость"
        ))

    if equity and total_liabilities:
        ratios.append(FinanceRatio(
            name="Коэффициент финансового левериджа",
            value=safe_div(total_liabilities, equity),
            unit="x",
            year=None,
            formula="Обязательства / Собственный капитал",
            category="Финансовая устойчивость"
        ))

    # РЕНТАБЕЛЬНОСТЬ
    revenue = get_metric(["Выручка", "Revenue", "Sales"])
    net_income = get_metric(["Чистая прибыль", "Net Income", "Net Profit"])
    ebitda = get_metric(["EBITDA"])
    operating_profit = get_metric(["Операционная прибыль", "EBIT", "Operating Profit"])

    if revenue and net_income:
        ratios.append(FinanceRatio(
            name="Рентабельность по чистой прибыли (ROS)",
            value=safe_div(net_income, revenue),
            unit="%",
            year=None,
            formula="Чистая прибыль / Выручка",
            category="Рентабельность"
        ))

    if revenue and operating_profit:
        ratios.append(FinanceRatio(
            name="Операционная рентабельность",
            value=safe_div(operating_profit, revenue),
            unit="%",
            year=None,
            formula="Операционная прибыль / Выручка",
            category="Рентабельность"
        ))

    if revenue and ebitda:
        ratios.append(FinanceRatio(
            name="Рентабельность по EBITDA",
            value=safe_div(ebitda, revenue),
            unit="%",
            year=None,
            formula="EBITDA / Выручка",
            category="Рентабельность"
        ))

    if net_income and equity:
        ratios.append(FinanceRatio(
            name="Рентабельность собственного капитала (ROE)",
            value=safe_div(net_income, equity),
            unit="%",
            year=None,
            formula="Чистая прибыль / Собственный капитал",
            category="Рентабельность"
        ))

    if net_income and total_assets:
        ratios.append(FinanceRatio(
            name="Рентабельность активов (ROA)",
            value=safe_div(net_income, total_assets),
            unit="%",
            year=None,
            formula="Чистая прибыль / Активы",
            category="Рентабельность"
        ))

    # ДЕЛОВАЯ АКТИВНОСТЬ
    if revenue and total_assets:
        ratios.append(FinanceRatio(
            name="Оборачиваемость активов",
            value=safe_div(revenue, total_assets),
            unit="x",
            year=None,
            formula="Выручка / Активы",
            category="Деловая активность"
        ))

    return ratios