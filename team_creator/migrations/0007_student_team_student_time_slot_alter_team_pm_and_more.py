# Generated by Django 4.0.1 on 2022-01-27 10:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('team_creator', '0006_team_time_slot'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Students', to='team_creator.team', verbose_name='Student team'),
        ),
        migrations.AddField(
            model_name='student',
            name='time_slot',
            field=models.ManyToManyField(blank=True, related_name='Students', to='team_creator.TimeSlot', verbose_name='Student time slot'),
        ),
        migrations.AlterField(
            model_name='team',
            name='pm',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Teams', to='team_creator.pm', verbose_name='Team PM'),
        ),
        migrations.AlterField(
            model_name='team',
            name='time_slot',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Teams', to='team_creator.timeslot', verbose_name='Team time slot'),
        ),
    ]