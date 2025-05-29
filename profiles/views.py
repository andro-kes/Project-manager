from rest_framework import generics, permissions
from profiles.models import Profile
from profiles.serializers import ProfileSerializer, ProfileUpdateSerializer

class ProfileDetailAPIView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Возвращает профиль текущего пользователя
        return self.request.user.profile

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']: #тут гпт подсказал так сделать
            return ProfileUpdateSerializer
        return ProfileSerializer
