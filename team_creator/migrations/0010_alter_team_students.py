# Generated by Django 4.0.1 on 2022-01-28 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team_creator', '0009_remove_team_students_team_students'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='Students', to='team_creator.Student', verbose_name='Team students'),
        ),
    ]