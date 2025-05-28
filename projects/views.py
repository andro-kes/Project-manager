from rest_framework import generics, permissions
from .permissions import IsTeamLead
from .models import Board, Project, Task
from .serializers import ProjectSerializer, BoardSerializer, TaskSerializer

class BaseProjectAPIView(generics.GenericAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

class CreateProjectAPIView(generics.CreateAPIView, BaseProjectAPIView):
    def get_serializer_context(self):
        return {'request': self.request}
    
    def perform_create(self, serializer):
        serializer.save()
    
class RetrieveProjectAPIView(BaseProjectAPIView, generics.RetrieveAPIView):
    queryset = Project.objects.all().prefetch_related("board")

class GetBoardAPIView(generics.RetrieveAPIView):
    queryset = Board.objects.all().prefetch_related("tasks")
    serializer_class = BoardSerializer    
    
class CreateTaskAPIView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeamLead]
    
    def perform_create(self, serializer):
        board_id = self.kwargs.get('board_id')
        board = Board.objects.get(pk=board_id) 
        serializer.save(board=board)

    def get_queryset(self):
        board_id = self.kwargs.get('board_id')
        if board_id is not None:
            return Task.objects.filter(board_id = board_id)
        return Task.objects.all()
    
class UpdateTaskAPIView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeamLead]
    lookup_field = 'pk'

    def get_queryset(self):
        board_id = self.kwargs.get('board_id') 
        if board_id:
            try:
                board = Board.objects.get(pk=board_id)
                project = board.project
                if self.request.user == project.team_lead:
                    return Task.objects.filter(board__project=project)  
            except Board.DoesNotExist:
                pass  
        return Task.objects.none()  
    
class DeleteTaskAPIView(generics.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer 
    permission_classes = [permissions.IsAuthenticated, IsTeamLead]
    lookup_field = 'pk'  

    def get_queryset(self):
        board_id = self.kwargs.get('board_id')  
        if board_id:
            try:
                board = Board.objects.get(pk=board_id)
                project = board.project
                if self.request.user == project.team_lead:
                    return Task.objects.filter(board__project=project)  
            except Board.DoesNotExist:
                pass 
        return Task.objects.none()  