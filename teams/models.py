from django.db import models


class TimeSlot(models.Model):
    timeslot = models.CharField(
        verbose_name="Timeslot",
        max_length=200,
    )

    def __str__(self):
        return self.timeslot


class PM(models.Model):
    name = models.CharField(verbose_name="Name", max_length=200)
    tg_username = models.CharField(verbose_name="Telegram username", max_length=200)
    discord_username = models.CharField(verbose_name="Discord username", max_length=200)
    timeslot = models.ManyToManyField(
        TimeSlot,
        verbose_name="Timeslot",
        max_length=200,
        related_name="PMs",
    )

    def __str__(self) -> str:
        return f"PM {self.name}"


class Student(models.Model):
    name = models.CharField(verbose_name="Name", max_length=200)
    level = models.CharField(verbose_name="Level", max_length=200)
    tg_username = models.CharField(verbose_name="Telegram username", max_length=200)
    discord_username = models.CharField(verbose_name="Discord username", max_length=200)
    is_far_east = models.BooleanField(
        verbose_name="User from Far Eastern Federal District", default=False
    )
    timeslot = models.ManyToManyField(
        TimeSlot,
        verbose_name="Student timeslot",
        related_name="Students",
        blank=True,
    )
    in_team = models.BooleanField(verbose_name="Student already in team", default=False)

    def __str__(self) -> str:
        return f"{self.name}, {self.tg_username}, {self.level}"


class Team(models.Model):
    pm = models.ForeignKey(
        PM,
        verbose_name="Team PM",
        related_name="Teams",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    timeslot = models.ForeignKey(
        TimeSlot,
        verbose_name="Team timeslot",
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
    level = models.CharField(
        verbose_name="Level",
        max_length=200,
    )

    def __str__(self):
        return f"Team {self.pk}, {self.pm}, {self.level}, {self.timeslot.timeslot}"
