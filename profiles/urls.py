from django.urls import path
from . import views

urlpatterns = [
    path('profiles/me', views.ProfileDetailAPIView.as_view(), name='profile-detail'),
]