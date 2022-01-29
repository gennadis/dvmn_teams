# Generated by Django 4.0.1 on 2022-01-28 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("teams", "0008_remove_student_team_team_students"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="team",
            name="students",
        ),
        migrations.AddField(
            model_name="team",
            name="students",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="Students",
                to="teams.Student",
                verbose_name="Team students",
            ),
        ),
    ]