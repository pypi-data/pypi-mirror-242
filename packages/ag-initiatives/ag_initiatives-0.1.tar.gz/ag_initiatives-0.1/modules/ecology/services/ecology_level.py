from typing import Dict

from modules.ecology.models import EcologyLevel, Survey, SurveyQuestion


def _get_groups(data: Dict, question: SurveyQuestion):
    result = []

    answers = question.answers.all()
    groups = (
        answers.exclude(group__exact="")
        .filter(group__isnull=False)
        .values_list("group", flat=True)
        .distinct()
    )

    for group in groups:
        result.append(
            {
                "id": group,
                "type": "GROUP",
                "answers": [answer.id for answer in answers.filter(group=group)],
            }
        )

    for answer in answers.exclude(group__in=groups):
        result.append({"type": "SINGLE", "answer": answer.id})


def get_ecology_level(percentage: int):
    if 80 <= percentage <= 100:
        return EcologyLevel.HIGH

    if 50 <= percentage <= 79:
        return EcologyLevel.MIDDLE

    if 0 <= percentage <= 49:
        return EcologyLevel.LOW

    return EcologyLevel.LOW
