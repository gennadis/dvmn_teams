from django.core.management.base import BaseCommand
from teams.models import TimeSlot, Student, PM, Team
from django.db.models import Count


def get_populated_teams():
    populated_teams = (
        Team.objects.annotate(students_in_team=Count("students"))
        .filter(
            students_in_team__gt=0,
        )
        .all()
    )
    for team in populated_teams:
        print(
            team.id,
            team.level,
            team.time_slot.time_slot,
            [s.name for s in team.students.all()],
        )


class Command(BaseCommand):
    help = "Some bot help information"

    def handle(self, *args, **kwargs):
        # create Student instance
        student = Student.objects.get(tg_username=input("Enter students tg_username "))
        print(f"Hello, {student.name}!")

        # get all available teams filtered by level and capacity
        available_teams = (
            Team.objects.annotate(students_in_team=Count("students"))
            .filter(
                level=student.level,
                students_in_team__lt=3,
            )
            .all()
        )
        print(f"Available teams IDs: {[team.pk for team in available_teams]}")

        # get available timeslots
        timeslots = [
            (team.time_slot.pk, team.pm.name, team.time_slot.time_slot)
            for team in available_teams
        ]
        print(f"Available teams timeslots: {timeslots}")

        # get user's timeslot choice primary key
        users_ts_choice = input("Choose timeslot primary key ")

        # get first team that fits by timeslot - from available teams
        users_team = available_teams.filter(time_slot=users_ts_choice).first()
        print(f"Your team ID is {users_team}")

        # add student to team and save
        users_team.students.add(student)
        users_team.save()
        student.in_team = True
        student.save()

        # get all team students
        print(
            f"Students in your team: {[student.name for student in users_team.students.all()]}"
        )

        # check all populated teams
        print("#" * 50)
        print("ALL TEAMS")
        get_populated_teams()

        # print(generate_level())
        # add_empty_teams()
        # teams = [team.level for team in Team.objects.all()]
        # student_levels = [s.level for s in Student.objects.all()]
        # counter = dict(Counter(student_levels))
        # for level, num in counter.items():
        #     counter[level] = count_divmod_three(num)
        # print(counter)
        # print(Counter(teams))
