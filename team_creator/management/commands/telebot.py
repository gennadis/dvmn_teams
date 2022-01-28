from django.core.management.base import BaseCommand
from team_creator.models import TimeSlot, Student, PM, Team


class Command(BaseCommand):
    help = "Some bot help information"

    def handle(self, *args, **kwargs):
        pass
