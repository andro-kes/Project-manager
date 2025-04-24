from django.contrib import admin
from .models import Task, Project, Board

admin.site.register(Task)
admin.site.register(Board)
admin.site.register(Project)
