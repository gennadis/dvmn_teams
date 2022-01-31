import json
import os
import random

from django.core.management.base import BaseCommand
from faker import Faker

FIXTURES_PATH = "./teams/fixtures/"

START_HOUR = 8
END_HOUR = 22
TIMESLOTS_TOTAL = 2 * (END_HOUR - START_HOUR)  # 1 hour == 2 timeslots

STUDENTS_TOTAL_COUNT = 50
PM_TOTAL_COUNT = 2
PM_TOTAL_TIMESLOTS = 5

TEAMS_TOTAL_COUNT = int(STUDENTS_TOTAL_COUNT / 3)


def save_json(data: list[dict], filename: str) -> str:
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

    return filename


def split_hours(start_hour: int, end_hour: int) -> list:
    intervals = []
    for hour in range(start_hour, end_hour):
        intervals.extend([f"{hour}:00 - {hour}:30", f"{hour}:30 - {hour+1}:00"])

    return intervals


def generate_timeslots_fixtures(filename: str, start_hour: int, end_hour: int) -> str:
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


def generate_pm_fixtures(filename: str, count: int, fake: Faker) -> str:
    pms = []
    for i in range(1, count + 1):
        pms.append(
            {
                "model": "teams.pm",
                "pk": i,
                "fields": {
                    "name": fake.name(),
                    "tg_username": f"@{fake.word()}_{fake.word()}",  # @word_word
                    "discord_username": f"{fake.word()}#{random.randint(1_000, 10_000)}",  # word#9876
                    # 18:00 - 22:00 timeslots for all PMs
                    "timeslot": [21, 22, 23, 24, 25, 26, 27, 28],
                },
            }
        )
    save_json(pms, filename)

    return filename


def generate_students_fixtures(filename: str, count: int, fake: Faker) -> str:
    students = []
    for i in range(1, count + 1):
        students.append(
            {
                "model": "teams.student",
                "pk": i,
                "fields": {
                    "name": fake.name(),
                    "level": random.choice(["novice", "novice+", "junior"]),
                    "tg_username": f"@{fake.word()}_{fake.word()}",  # @word_word
                    "discord_username": f"{fake.word()}#{random.randint(1_000, 10_000)}",  # word#9876
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
        os.makedirs(FIXTURES_PATH, exist_ok=True)

        generate_timeslots_fixtures(
            os.path.join(FIXTURES_PATH, "timeslots.json"), START_HOUR, END_HOUR
        )
        generate_pm_fixtures(
            os.path.join(FIXTURES_PATH, "pms.json"), PM_TOTAL_COUNT, fake
        )
        generate_students_fixtures(
            os.path.join(FIXTURES_PATH, "students.json"), STUDENTS_TOTAL_COUNT, fake
        )
