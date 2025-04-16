from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    team_lead = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects_lead")
    members = models.ManyToManyField(User, related_name="projects_members", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    
class Board(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="board")
    
    def __str__(self):
        return f'{self.project.title}'
    
class Task(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(
        max_length=20,
        choices=[
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        ],
        default="medium",
    )
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="tasks")
    
    def __str__(self):
        return self.head