import random
from collections import Counter
from typing import Generator

from django.core.management.base import BaseCommand
from django.db.models import QuerySet

from teams.models import TimeSlot, Student, PM, Team


def calculate_divmod_three(num: int) -> int:
    quotient, remainder = divmod(num, 3)
    if remainder:
        return quotient + 1
    return quotient


def generate_team_level(students: QuerySet) -> Generator:
    student_levels = [student.level for student in students]

    levels_counter = Counter(student_levels)
    for level, count in levels_counter.items():
        levels_counter[level] = calculate_divmod_three(count)

    team_levels = []
    for level, count in levels_counter.items():
        team_levels.extend([level] * count)
    random.shuffle(team_levels)

    return (level for level in team_levels)


def generate_empty_teams(students: QuerySet, pms: QuerySet) -> QuerySet:
    team_level = generate_team_level(students)
    for pm in pms:
        for pm_timeslot in pm.timeslot.all():
            Team.objects.create(pm=pm, timeslot=pm_timeslot, level=next(team_level))

    return Team.objects.all()


class Command(BaseCommand):
    help = "Make empty teams for each PM and his\her timeslot"

    def handle(self, *args, **kwargs):
        students = Student.objects.all()
        pms = PM.objects.all()
        empty_teams = generate_empty_teams(students, pms)
