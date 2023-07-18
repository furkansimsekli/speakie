from django.db import models
from django.utils.text import slugify
from unidecode import unidecode

from users.models import User

# TODO: Move these type of constant configs to somewhere else
LEVEL_CHOICES = (
    (1, 'Easy'),
    (2, 'Intermediate'),
    (3, 'Hard')
)


class Course(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True, blank=True, allow_unicode=True)
    description = models.CharField(max_length=255)
    flag_picture = models.ImageField(default='default_flag_pic.jpg', upload_to='flag_pictures/')
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        base_slug = slugify(unidecode(self.title))[:250]  # 250 chars for title, 1 char for '-', and 4 char for number
        self.slug = base_slug
        slug_num = 1

        while Course.objects.filter(slug=self.slug).exists():
            self.slug = f'{base_slug}-{slug_num}'
            slug_num += 1

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class TranslationPractice(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True, allow_unicode=True)
    question = models.CharField(max_length=255, default='')
    answer = models.CharField(max_length=255, default='')
    choice_1 = models.CharField(max_length=255, default='')
    choice_2 = models.CharField(max_length=255, default='')
    choice_3 = models.CharField(max_length=255, default='')
    difficulty = models.SmallIntegerField(default=0, choices=LEVEL_CHOICES)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        base_slug = slugify(unidecode(self.title))[:250]  # 250 chars for title, 1 char for '-', and 4 char for number
        self.slug = base_slug
        slug_num = 1

        while TranslationPractice.objects.filter(slug=self.slug).exists():
            self.slug = f'{base_slug}-{slug_num}'
            slug_num += 1

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class SpeakingPractice(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True, blank=True, allow_unicode=True)
    paragraph = models.TextField()
    difficulty = models.SmallIntegerField(default=0, choices=LEVEL_CHOICES)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        base_slug = slugify(unidecode(self.title))[:250]  # 250 chars for title, 1 char for '-', and 4 char for number
        self.slug = base_slug
        slug_num = 1

        while SpeakingPractice.objects.filter(slug=self.slug).exists():
            self.slug = f'{base_slug}-{slug_num}'
            slug_num += 1

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class TranslationPracticeSolved(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    practice = models.ForeignKey(TranslationPractice, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'practice')
