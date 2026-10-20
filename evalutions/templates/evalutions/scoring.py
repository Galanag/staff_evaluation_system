
from decimal import Decimal, ROUND_HALF_UP

from models import EvaluationSubmission


ACADEMIC_WEIGHTS = {
    "STUDENT": Decimal("40"),
    "HOD": Decimal("35"),
    "PEER": Decimal("15"),
    "SELF": Decimal("10"),
}

ADMINISTRATIVE_SECTION_WEIGHTS = {
    "Work Plan Execution": Decimal("70"),
    "Work Process Behaviors": Decimal("30"),
}


def average_submission_score(submission):
    """
    Average valid ratings from 0 to 5.
    NA and unanswered questions are excluded.
    """
    responses = submission.responses.filter(
        not_applicable=False,
        score__isnull=False,
    )

    scores = list(responses.values_list("score", flat=True))

    if not scores:
        return None

    average = sum(scores) / len(scores)
    return Decimal(str(average)).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )


def normalized_percentage(average_score):
    """
    Convert an average score out of 5 into a percentage.
    """
    if average_score is None:
        return None

    return (
        average_score * Decimal("20")
    ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def academic_final_score(staff_member, cycle):
    """
    Calculate the weighted academic result.

    The final result is available only after all four
    evaluator categories have submitted valid scores.
    """
    submissions = EvaluationSubmission.objects.filter(
        staff_member=staff_member,
        cycle=cycle,
        status__in=[
            EvaluationSubmission.Status.SUBMITTED,
            EvaluationSubmission.Status.REVIEWED,
        ],
    )

    results = {}
    missing = []

    for evaluator_type, weight in ACADEMIC_WEIGHTS.items():
        matching = submissions.filter(
            evaluator_type=evaluator_type
        )

        scores = [
            average_submission_score(submission)
            for submission in matching
        ]
        scores = [score for score in scores if score is not None]

        if not scores:
            missing.append(evaluator_type)
            continue

        # Multiple submissions in one evaluator category are
        # averaged before applying that category's weight.
        category_average = sum(scores) / len(scores)
        category_percentage = normalized_percentage(category_average)

        results[evaluator_type] = {
            "average_out_of_5": category_average.quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            ),
            "weight": weight,
            "weighted_points": (
                category_percentage * weight / Decimal("100")
            ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
        }

    if missing:
        return {
            "complete": False,
            "missing_categories": missing,
            "categories": results,
            "final_score": None,
        }

    final_score = sum(
        item["weighted_points"] for item in results.values()
    )

    return {
        "complete": True,
        "missing_categories": [],
        "categories": results,
        "final_score": final_score.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        ),
    }


def administrative_final_score(section_averages):
    """
    section_averages example:
    {
        "Work Plan Execution": Decimal("4.20"),
        "Work Process Behaviors": Decimal("3.80"),
    }

    Both averages must be on the 0-to-5 scale.
    """
    required_sections = set(ADMINISTRATIVE_SECTION_WEIGHTS)
    missing = required_sections - set(section_averages)

    if missing:
        return {
            "complete": False,
            "missing_sections": sorted(missing),
            "final_score": None,
        }

    total = Decimal("0")

    for section, weight in ADMINISTRATIVE_SECTION_WEIGHTS.items():
        average = Decimal(str(section_averages[section]))

        if not Decimal("0") <= average <= Decimal("5"):
            raise ValueError(
                f"{section} average must be between 0 and 5."
            )

        weighted_points = (
            average * Decimal("20") * weight / Decimal("100")
        )
        total += weighted_points

    return {
        "complete": True,
        "missing_sections": [],
        "final_score": total.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        ),
    }
