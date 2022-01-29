from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class TimeSlot(models.Model):
    time_slot = models.CharField(
        verbose_name="Time slot",
        max_length=200,
    )

    def __str__(self):
        return f"Time slot {self.time_slot}"


class PM(models.Model):
    name = models.CharField(verbose_name="Name", max_length=200)
    tg_username = models.CharField(verbose_name="Telegram username", max_length=200)
    discord_username = models.CharField(verbose_name="Discord username", max_length=200)
    time_slots = models.ManyToManyField(
        TimeSlot,
        verbose_name="Time slot",
        max_length=200,
        related_name="PMs",
    )

    def __str__(self) -> str:
        return f"PM {self.name}, {self.tg_username}"


class Student(models.Model):
    name = models.CharField(verbose_name="Name", max_length=200)
    level = models.CharField(verbose_name="Level", max_length=200)
    tg_username = models.CharField(verbose_name="Telegram username", max_length=200)
    discord_username = models.CharField(verbose_name="Discord username", max_length=200)
    is_far_east = models.BooleanField(
        verbose_name="User from Far Eastern Federal District", default=False
    )
    time_slot = models.ManyToManyField(
        TimeSlot,
        verbose_name="Student time slot",
        related_name="Students",
        blank=True,
    )
    in_team = models.BooleanField(verbose_name="Studetn already in team", default=False)

    def __str__(self) -> str:
        return f"Student {self.name}, tg: {self.tg_username}"


class Team(models.Model):
    pm = models.ForeignKey(
        PM,
        verbose_name="Team PM",
        related_name="Teams",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    time_slot = models.ForeignKey(
        TimeSlot,
        verbose_name="Team time slot",
        related_name="Teams",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    students = models.ManyToManyField(
        Student,
        verbose_name="Team students",
        related_name="Students",
        blank=True,
    )
    counter = models.IntegerField(
        verbose_name="Students in Team",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(3),
        ],
        default=0,
    )
    level = models.CharField(
        verbose_name="Level",
        max_length=200,
    )

    def __str__(self):
        return f"Team {self.pk}"
