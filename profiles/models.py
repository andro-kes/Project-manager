from django.db import models

class Profile(models.Model):
    user = models.OneToOneField("users.User", on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    skills = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    tg = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"