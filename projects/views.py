from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from django.http import HttpResponse, JsonResponse
from .permissions import IsTeamLead
from .models import Board, Project, Task
from users.models import User
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
    
def add_member(project_id, user_id):
    try:
        project = get_object_or_404(Project, pk=project_id) 
        user = get_object_or_404(User, pk=user_id) 

        if user in project.members.all():
            return JsonResponse({"message: Пользователь уже в проекте"}, status=200)

        project.members.add(user)
        project.save() 

        return JsonResponse(project.members, status=200)

    except Exception as e:
        print(f"Error adding member to project: {e}") 
        return JsonResponse({"message": f"Ошибка {e}"}, status=500)

def change_task_status(request, task_id):
    if request.method == 'POST':  
        try:
            task = get_object_or_404(Task, pk=task_id) 
            new_status = request.POST.get('status')  

            if new_status in [choice[0] for choice in Task.status.field.choices]: 
                task.status = new_status
                task.save()
                return JsonResponse({"new status": task.status}, status=200)  # Success
            else:
                return JsonResponse({'error': 'Неверный статус'}, status=400) 

        except Exception as e:
            print(f"Error changing task status: {e}")
            return JsonResponse({'error': 'Failed to update task status.'}, status=500) # Internal Server Error

    else:
        return HttpResponse(status=405)  