import math

from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bio = models.TextField(default='', max_length=255)
    profile_picture = models.ImageField(default='default_profile_pic.jpg', upload_to='profile_pictures/')
    score = models.PositiveIntegerField(default=1)
    level = models.PositiveIntegerField()
    is_moderator = models.BooleanField(default=False)

    def __str__(self):
        print(f'{self.username} - Moderator: {self.is_moderator}')

    def save(self, *args, **kwargs):
        self.level = self.calculate_level()
        super().save()
        img = Image.open(self.profile_picture.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_picture.path)

    def calculate_level(self):
        return math.ceil(math.log(1 + 0.005 * self.score, 1.5))
