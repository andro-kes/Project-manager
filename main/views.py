from rest_framework import generics, permissions
from . import serializers
from projects.models import Project
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class GetUserProjectsAPIView(generics.ListAPIView):
    serializer_class = serializers.ProjectListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        queryset = Project.objects.filter(
            Q(team_lead=user) | Q(members=user)
        ).distinct()
        return queryset
