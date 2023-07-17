from django.db import models
from django.utils.text import slugify

# TODO: Move these type of constant configs to somewhere else
LEVEL_CHOICES = (
    (1, 'Easy'),
    (2, 'Intermediate'),
    (3, 'Hard')
)


class Course(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.CharField(max_length=255)
    flag_picture = models.ImageField(default='default_flag_pic.jpg', upload_to='flag_pictures/')
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class TranslationPractice(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    question = models.CharField(max_length=255, default='')
    answer = models.CharField(max_length=255, default='')
    choice_1 = models.CharField(max_length=255, default='')
    choice_2 = models.CharField(max_length=255, default='')
    choice_3 = models.CharField(max_length=255, default='')
    difficulty = models.SmallIntegerField(default=0, choices=LEVEL_CHOICES)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)[:256]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class SpeakingPractice(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    paragraph = models.TextField()
    difficulty = models.SmallIntegerField(default=0, choices=LEVEL_CHOICES)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
