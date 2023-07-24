from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from unidecode import unidecode


@receiver(pre_save)
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
