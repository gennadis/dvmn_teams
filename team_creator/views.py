from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the team_creator index.")


def student_detail(request, student_id):
    return HttpResponse("You're looking at student %s." % student_id)


def student_time_slots(request, student_id):
    response = "Student's time slots are %s."
    return HttpResponse(response % student_id)


def student_team(request, student_id):
    return HttpResponse("Student's team is %s." % student_id)
