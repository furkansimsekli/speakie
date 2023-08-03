from django.db import models

from users.models import User


class Notification(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(default='')
    url = models.URLField(default='#', )
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.owner} - {self.message} - {self.is_read}'
