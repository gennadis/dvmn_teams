import random
from collections import Counter
from typing import Generator

from django.core.management.base import BaseCommand
from team_creator.models import TimeSlot, Student, PM, Team


def generate_team_level() -> Generator:
    student_levels = [s.level for s in Student.objects.all()]

    level_count = dict(Counter(student_levels))
    for level, num in level_count.items():
        level_count[level] = count_divmod_three(num)

    team_levels = []
    for level, count in level_count.items():
        team_levels.extend([level] * count)
    random.shuffle(team_levels)

    return (x for x in team_levels)


def count_divmod_three(num: int) -> int:
    quotient, remainder = divmod(num, 3)
    return quotient + 1 if remainder else quotient


def generate_empty_teams() -> None:
    team_level = generate_team_level()
    for pm in PM.objects.all():
        for ts in pm.timeslot.all():
            Team.objects.create(pm=pm, timeslot=ts, level=next(team_level))


class Command(BaseCommand):
    help = "Make some teams"

    def handle(self, *args, **kwargs):
        generate_empty_teams()
