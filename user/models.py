from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(default='default_profile_pic.jpg', upload_to='profile_pictures/')
    score = models.PositiveIntegerField(default=1)
    is_moderator = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.username} - Moderator: {self.is_moderator}'

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.profile_picture.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_picture.path)
