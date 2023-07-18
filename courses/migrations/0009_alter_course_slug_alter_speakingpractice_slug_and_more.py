# Generated by Django 4.2.3 on 2023-07-18 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_alter_course_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='slug',
            field=models.SlugField(allow_unicode=True, blank=True, max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='speakingpractice',
            name='slug',
            field=models.SlugField(allow_unicode=True, blank=True, max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='translationpractice',
            name='slug',
            field=models.SlugField(allow_unicode=True, blank=True, max_length=255, unique=True),
        ),
    ]