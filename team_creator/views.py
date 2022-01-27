from django.http import HttpResponse

from .models import Student, TimeSlot, PM


def index(request):
    students_list = Student.objects.all()
    names = ", ".join([s.name for s in students_list])

    pm_list = PM.objects.all()
    pm_names = ", ".join([pm.name for pm in pm_list])

    time_slots_list = TimeSlot.objects.all()
    time_slots = ", ".join([t.time_slot for t in time_slots_list])

    output = f"Students: {names}, ||| PMs: {pm_names}, ||| Timeslots: {time_slots}"

    return HttpResponse(output)


def student_detail(request, student_id):
    return HttpResponse("You're looking at student %s." % student_id)


def student_time_slots(request, student_id):
    response = "Student's time slots are %s."
    return HttpResponse(response % student_id)


def student_team(request, student_id):
    return HttpResponse("Student's team is %s." % student_id)
