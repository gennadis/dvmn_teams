from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count

from .models import PM, TimeSlot, Student, Team


def index(request):
    """View function for home page of site."""

    populated_teams = (
        Team.objects.annotate(students_in_team=Count("students"))
        .filter(
            students_in_team__gt=0,
        )
        .all()
    )
    # for team in populated_teams:
    #     print(
    #         team.id,
    #         team.level,
    #         team.timeslot.timeslot,
    #         [s.name for s in team.students.all()],
    #     )

    context = {
        "populated_teams": populated_teams,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, "index.html", context=context)
