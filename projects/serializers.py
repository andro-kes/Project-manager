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
    assigned_to_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,  
        source='assigned_to',  
        allow_null=True 
    )
    class Meta:
        model = Task
        fields = ("id", "title", "description", "priority", "created_at", "board", "assigned_to", "assigned_to_id")
        
class BoardSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    class Meta:
        model = Board
        fields = ("id", "project", "tasks")
        
class ProjectSerializer(serializers.ModelSerializer):
    boards = BoardSerializer(read_only=True, many=True)
    members = UserSerializer(many=True, read_only=True)
    team_lead = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ("id", "title", "description", "boards", "team_lead", "members")

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['team_lead'] = request.user 
        else:
            raise serializers.ValidationError("Пользователь не зарегистрирован.")

        members_data = validated_data.pop('members', [])
        project = Project.objects.create(**validated_data)
        Board.objects.create(project=project)

        return project