from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField()
    level = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    profile_picture = models.ImageField(default='default_profile_pic.jpg ', upload_to='profile_pictures/')

    def __str__(self):
        print(self.user.username)


class ModeratorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField()
    profile_picture = models.ImageField(default='default_profile_pic.jpg ', upload_to='profile_pictures/')

    def __str__(self):
        print(self.user.username)
