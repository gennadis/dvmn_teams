import site
from django.contrib import admin

from .models import PM, Student, Team

# Register your models here.

admin.site.register(Student)
admin.site.register(PM)
admin.site.register(Team)
