from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    date_joined = models.DateTimeField(default=timezone.now)
    description = models.TextField(default='')

    def __str__(self):
        return f'{self.user.username} Profile'