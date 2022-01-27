from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

import team_creator

from .models import Student, TimeSlot, PM


def index(request):
    students_list = Student.objects.all()
    context = {
        "students_list": students_list,
    }
    print(students_list)
    return render(request, "team_creator/index.html", context)


def student_detail(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    return render(request, "team_creator/detail.html", {"student": student})


def student_time_slots(request, student_id):
    response = "Student's time slots are %s."
    time_slots = get_object_or_404(TimeSlot.objects.all(), pk=student_id)
    return HttpResponse(response % time_slots)


def student_team(request, student_id):
    return HttpResponse("Student's team is %s." % student_id)


def choose_time_slot(request, time_slot_id):
    time_slot = get_object_or_404(TimeSlot, pk=time_slot_id)
    try:
        selected_choice = time_slot.choice_set.get(pk=request.POST["choice"])
    except (KeyError, TimeSlot.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "team_creator/detail.html",
            {
                "time_slot": time_slot,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.time_slot += f" {time_slot} "
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("team_creator:slots", args=(time_slot.id,)))
