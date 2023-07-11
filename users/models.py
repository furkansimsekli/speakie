from django.contrib.auth.models import User
from django.db import models
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default='')
    profile_picture = models.ImageField(default='default_profile_pic.jpg', upload_to='profile_pictures/')

    def __str__(self):
        print(self.user.username)

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.profile_picture.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_picture.path)


class Student(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)

    def __str__(self):
        print(f'{self.profile.user.username} - {self.score}')


class Moderator(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    def __str__(self):
        print({self.profile.user.username})
