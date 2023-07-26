from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from unidecode import unidecode

from .models import Course, TranslationPractice, SpeakingPractice


@receiver(pre_save, sender=Course)
@receiver(pre_save, sender=TranslationPractice)
@receiver(pre_save, sender=SpeakingPractice)
def change_slug(sender, instance, **kwargs):
    try:
        obj = sender.objects.get(pk=instance.pk)

        if obj.title != instance.title:
            base_slug = slugify(unidecode(instance.title))[:100]
            course_count = sender.objects.filter(slug__startswith=base_slug).count()

            if course_count > 0:
                instance.slug = f'{base_slug}-{course_count}'
            else:
                instance.slug = base_slug
    except sender.DoesNotExist:
        base_slug = slugify(unidecode(instance.title))[:100]
        course_count = sender.objects.filter(slug__startswith=base_slug).count()

        if course_count > 0:
            instance.slug = f'{base_slug}-{course_count}'
        else:
            instance.slug = base_slug
