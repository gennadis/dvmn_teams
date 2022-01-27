from django.http import HttpResponse, Http404

from django.shortcuts import render, get_object_or_404

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
    return HttpResponse(response % student_id)


def student_team(request, student_id):
    return HttpResponse("Student's team is %s." % student_id)
