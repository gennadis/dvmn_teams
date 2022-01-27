from django.urls import path

from . import views

app_name = "team_creator"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:student_id>/", views.student_detail, name="detail"),
    # ex: /student/5/timeslot/
    # path("<int:student_id>/timeslot/", views.student_time_slots, name="time slots"),
    # ex: /student/5/team/
    path("<int:student_id>/team/", views.student_team, name="team"),
    path("<int:student_id>/timeslot/", views.student_time_slots, name="time slots"),
]
