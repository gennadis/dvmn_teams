"""Run this command to import generated fixtures:

python manage.py loaddata students.json pms.json timeslots.json
"""
import os
import json
import random

from django.core.management.base import BaseCommand
from faker import Faker

# timeslots
START_HOUR = 8
END_HOUR = 22
TIMESLOTS_TOTAL = 2 * (END_HOUR - START_HOUR)

# students
STUDENTS_TOTAL_COUNT = 50

# pm
PM_TOTAL_COUNT = 2
PM_TOTAL_TIMESLOTS = 5

# teams
TEAMS_TOTAL_COUNT = int(STUDENTS_TOTAL_COUNT / 3)


def save_json(data: list[dict], filename: str) -> None:
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


def split_hours(start: int, end: int) -> list:
    intervals = []
    for hour in range(start, end):
        intervals.extend([f"{hour}:00 - {hour}:30", f"{hour}:30 - {hour+1}:00"])
    return intervals


def generate_timeslots_json(filename: str, start_hour: int, end_hour: int) -> str:
    timeslots = []
    for count, timeslot in enumerate(split_hours(start_hour, end_hour), start=1):
        timeslots.append(
            {
                "model": "teams.timeslot",
                "pk": count,
                "fields": {"timeslot": timeslot},
            }
        )
    save_json(timeslots, filename)
    return filename


def generate_pm_json(filename: str, count: int, fake: Faker) -> str:
    pms = []
    for i in range(1, count + 1):
        pms.append(
            {
                "model": "teams.pm",
                "pk": i,
                "fields": {
                    "name": fake.name(),
                    "tg_username": f"@{fake.word()}_{fake.word()}",
                    "discord_username": f"@{fake.word()}#1234",
                    # 18:00 - 22:00 timeslots for all PMs
                    "timeslot": [21, 22, 23, 24, 25, 26, 27, 28],
                },
            }
        )
    save_json(pms, filename)
    return filename


def generate_students_json(filename: str, count: int, fake: Faker) -> str:
    students = []
    for i in range(1, count + 1):
        students.append(
            {
                "model": "teams.student",
                "pk": i,
                "fields": {
                    "name": fake.name(),
                    "level": random.choice(["novice", "novice+", "junior"]),
                    "tg_username": f"@{fake.word()}_{fake.word()}",
                    "discord_username": f"{fake.word()}#{random.randint(1_000, 10_000)}",
                    "is_far_east": random.choice([True, False]),
                    "timeslot": [],
                    "in_team": False,
                },
            }
        )
    save_json(students, filename)
    return filename


class Command(BaseCommand):
    help = "Generate fake students, pms, timeslots data."

    def handle(self, *args, **kwargs):
        fake = Faker()
        os.makedirs("./teams/fixtures/", exist_ok=True)
        generate_timeslots_json("./teams/fixtures/timeslots.json", START_HOUR, END_HOUR)
        generate_pm_json("./teams/fixtures/pms.json", PM_TOTAL_COUNT, fake)
        # generate_teams_json("./teams/fixtures/teams.json", TEAMS_TOTAL_COUNT)
        generate_students_json(
            "./teams/fixtures/students.json", STUDENTS_TOTAL_COUNT, fake
        )
