from django.db import models

from users.models import User

# TODO: Move these type of constant configs to somewhere else
LEVEL_CHOICES = (
    (1, 'Easy'),
    (2, 'Intermediate'),
    (3, 'Hard')
)


class Course(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, allow_unicode=True)
    description = models.CharField(max_length=255)
    flag_picture = models.ImageField(default='default_flag_pic.jpg', upload_to='flag_pictures/')
    language_code = models.CharField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class TranslationPractice(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, allow_unicode=True)
    question = models.CharField(max_length=255, default='')
    answer = models.CharField(max_length=255, default='')
    choice_1 = models.CharField(max_length=255, default='')
    choice_2 = models.CharField(max_length=255, default='')
    choice_3 = models.CharField(max_length=255, default='')
    difficulty = models.SmallIntegerField(default=0, choices=LEVEL_CHOICES)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class SpeakingPractice(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, allow_unicode=True)
    paragraph = models.TextField()
    difficulty = models.SmallIntegerField(default=0, choices=LEVEL_CHOICES)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class TranslationPracticeSolved(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    practice = models.ForeignKey(TranslationPractice, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'practice')

    def __str__(self):
        return f'{self.user} - {self.practice}'


class SpeakingPracticeSolved(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    practice = models.ForeignKey(SpeakingPractice, on_delete=models.CASCADE)
    point = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'practice')

    def __str__(self):
        return f'{self.user} - {self.practice}'


class AudioRecord(models.Model):
    audio_file = models.FileField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    practice = models.ForeignKey(SpeakingPractice, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} - {self.practice} - {self.audio_file}'
