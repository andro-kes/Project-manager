from django.contrib.auth.models import AbstractUser
from profiles.models import Profile


class User(AbstractUser):
    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args, **kwargs)
        if created:
            Profile.objects.get_or_create(user=self)
