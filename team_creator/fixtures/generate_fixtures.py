"""Run this command to import generated fixtures:

python manage.py loaddata students.json pms.json teams.json timeslots.json
"""

import json
import random

from faker import Faker

# time slots
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
    for count, time_slot in enumerate(split_hours(start_hour, end_hour), start=1):
        timeslots.append(
            {
                "model": "team_creator.timeslot",
                "pk": count,
                "fields": {"time_slot": time_slot},
            }
        )
    save_json(timeslots, filename)
    return filename


def generate_pm_json(filename: str, count: int, fake: Faker) -> str:
    pms = []
    for i in range(1, count + 1):
        pms.append(
            {
                "model": "team_creator.pm",
                "pk": i,
                "fields": {
                    "name": fake.name(),
                    "tg_username": f"@{fake.word()}_{fake.word()}",
                    "discord_username": f"@{fake.word()}#1234",
                    "time_slots": [],
                },
            }
        )
    save_json(pms, filename)
    return filename


def generate_teams_json(filename: str, count: int):
    teams = []
    for i in range(1, count + 1):
        teams.append(
            {
                "model": "team_creator.team",
                "pk": i,
                "fields": {
                    "pm": None,
                    "time_slot": None,
                    "students": [],
                },
            }
        )
    save_json(teams, filename)
    return filename


def generate_students_json(filename: str, count: int, fake: Faker) -> str:
    students = []
    for i in range(1, count + 1):
        students.append(
            {
                "model": "team_creator.student",
                "pk": i,
                "fields": {
                    "name": fake.name(),
                    "level": random.choice(["novice", "novice+", "junior"]),
                    "tg_username": f"@{fake.word()}",
                    "discord_username": f"{fake.word()}#{random.randint(1_000, 10_000)}",
                    "is_far_east": random.choice([True, False]),
                    "time_slot": [],
                },
            }
        )
    save_json(students, filename)
    return filename


def main():
    fake = Faker()
    generate_timeslots_json(
        "./team_creator/fixtures/timeslots.json", START_HOUR, END_HOUR
    )
    generate_pm_json("./team_creator/fixtures/pms.json", PM_TOTAL_COUNT, fake)
    generate_teams_json("./team_creator/fixtures/teams.json", TEAMS_TOTAL_COUNT)
    generate_students_json(
        "./team_creator/fixtures/students.json", STUDENTS_TOTAL_COUNT, fake
    )


if __name__ == "__main__":
    main()
