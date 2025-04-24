from rest_framework import permissions

class IsTeamLead(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        board_id = view.kwargs.get('board_id') # Получаем из urls пока что
        if not board_id:
            return False 

        try:
            from .models import Board
            board = Board.objects.get(pk=board_id)
        except Board.DoesNotExist:
            return False 

        project = board.project
        return project.team_lead == request.user