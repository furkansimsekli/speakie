from django.db import models

# TODO: Move these type constant configs to somewhere else
# TODO: Do I need for course names too?

LEVEL_CHOICES = (
    (1, 'Easy'),
    (2, 'Intermediate'),
    (3, 'Hard')
)


class Course(models.Model):
    name = models.CharField(max_length=32)
    flag = models.ImageField(default='default_flag_pic.jpg', upload_to='flag_pictures')
    models.SlugField

    def __str__(self):
        return self.name


class TranslationPractice(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question = models.CharField(max_length=256)
    answer = models.CharField(max_length=256)
    difficulty = models.SmallIntegerField(default=0, choices=LEVEL_CHOICES)

    def __str__(self):
        return self.question
