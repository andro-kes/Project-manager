from rest_framework import serializers
from profiles.models import Profile
from users.serializers import UserSerializer

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'bio', 'skills', 'phone']
        read_only_fields = ['id', 'user']


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['bio', 'skills', 'phone'] #, 'avatar'
