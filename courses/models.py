from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class TranslationPractice(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question = models.CharField(max_length=256)
    answer = models.CharField(max_length=256)

    def __str__(self):
        return self.question
