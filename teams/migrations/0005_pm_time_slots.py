# Generated by Django 4.0.1 on 2022-01-27 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("teams", "0004_timeslot"),
    ]

    operations = [
        migrations.AddField(
            model_name="pm",
            name="time_slots",
            field=models.ManyToManyField(
                max_length=200,
                related_name="PMs",
                to="teams.TimeSlot",
                verbose_name="Time slot",
            ),
        ),
    ]