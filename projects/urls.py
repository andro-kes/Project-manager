from django.urls import path
from . import views

urlpatterns = [
    path("projects/create", views.CreateProjectAPIView.as_view(), name="create_project"),
    path("projects/<int:pk>", views.GetProjectAPIView.as_view(), name='get_project'),
    path("projects/board/<int:pk>", views.GetBoardAPIView.as_view(), name="get_board"),
]