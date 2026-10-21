"""Pure-Python evaluation scoring utilities (no Django dependency)."""
from decimal import Decimal, ROUND_HALF_UP

WEIGHT_BY_FORM = {"student": 40, "department_head": 35, "peer": 15, "self": 10}


def numeric_ratings(ratings):
    values = []
    for value in (ratings or {}).values():
        try:
            if value is None or str(value).strip().upper() in {"", "NA", "N/A"}:
                continue
            number = Decimal(str(value))
            if Decimal("0") <= number <= Decimal("5"):
                values.append(number)
        except Exception:
            continue
    return values


def average_rating(ratings):
    values = numeric_ratings(ratings)
    if not values:
        return Decimal("0.00")
    return (sum(values, Decimal("0")) / Decimal(len(values))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def weighted_score(form_type, ratings):
    average = average_rating(ratings)
    weight = Decimal(WEIGHT_BY_FORM.get(form_type, 0))
    return (average * weight / Decimal("5")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def category_average(category, ratings):
    keys = [item["key"] for item in category.get("items", [])]
    values = numeric_ratings({key: (ratings or {}).get(key) for key in keys})
    if not values:
        return None
    return (sum(values, Decimal("0")) / Decimal(len(values))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
