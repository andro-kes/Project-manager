from rest_framework import generics, permissions
from .models import Board, Project
from .serializers import ProjectSerializer, BoardSerializer

class BaseProjectAPIView(generics.GenericAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

class CreateProjectAPIView(BaseProjectAPIView, generics.CreateAPIView):
    pass
    
class RetrieveProjectAPIView(BaseProjectAPIView, generics.RetrieveAPIView):
    queryset = Project.objects.all().prefetch_related("board")

class GetBoardAPIView(generics.RetrieveAPIView):
    queryset = Board.objects.all().prefetch_related("tasks")
    serializer_class = BoardSerializer    