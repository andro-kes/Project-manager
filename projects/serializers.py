from rest_framework import serializers
from .models import Board, Task, Project
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")
        
class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    class Meta:
        model = Task
        fields = ("id", "title", "description", "priority", "created_at", "board", "assigned_to")
        
class BoardSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    class Meta:
        model = Board
        fields = ("id", "project", "tasks")
        
class ProjectSerializer(serializers.ModelSerializer):
    boards = BoardSerializer(read_only = True)
    members = UserSerializer(many=True, read_only = True)
    team_lead = UserSerializer(read_only=True)
    
    class Meta:
        model = Project
        fields = ("id", "title", "description", "boards", "team_lead", "members")
        
    def create(self, validated_data):
      project = Project.objects.create(**validated_data)
      Board.objects.create(project = project)
      return project