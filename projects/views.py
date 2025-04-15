from rest_framework import generics, permissions
from .models import Board, Project
from .serializers import ProjectSerializer, BoardSerializer

class BaseProjectAPIView(generics.GenericAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

class CreateProjectAPIView(BaseProjectAPIView, generics.CreateAPIView):
    def perform_create(self, serializer):
        project = serializer.save()
        Board.objects.create(project=project)
    
class GetProjectAPIView(BaseProjectAPIView, generics.RetrieveAPIView):
    pass

class GetBoardAPIView(generics.RetrieveAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer    