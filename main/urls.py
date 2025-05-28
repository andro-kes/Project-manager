from django.urls import path
from . import views

urlpatterns = [
    path("", views.GetUserProjectsAPIView.as_view(), name="user_projects"),
]
