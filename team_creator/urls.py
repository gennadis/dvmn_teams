from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:student_id>/", views.student_detail, name="detail"),
    # ex: /polls/5/results/
    path("<int:student_id>/timeslot/", views.student_time_slots, name="time slots"),
    # ex: /polls/5/vote/
    path("<int:student_id>/team/", views.student_team, name="team"),
]
