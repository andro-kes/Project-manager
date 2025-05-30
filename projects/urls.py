from django.urls import path
from . import views

urlpatterns = [
    path("projects/create", views.CreateProjectAPIView.as_view(), name="create_project"),
    path("projects/<int:pk>", views.RetrieveProjectAPIView.as_view(), name='get_project'),
    path("projects/board/<int:pk>", views.GetBoardAPIView.as_view(), name="get_board"),
    path("projects/<int:board_id>/tasks/create", views.CreateTaskAPIView.as_view(), name="create_task"),
    path("projects/board/<int:board_id>/tasks/<int:pk>/update", views.UpdateTaskAPIView.as_view(), name="update_task"),
    path("projects/board/<int:board_id>/tasks/<int:pk>/delete", views.DeleteTaskAPIView.as_view(), name="delete_task"),
    path("projects/<int:pk>/add_member/<int:pk>", views.add_member, name="add_member"),
    path("projects/tasks/<int:pk>/change_status/<int:pk>", views.change_task_status, name="change_status"),
]