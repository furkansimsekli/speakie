# Generated by Django 4.2.3 on 2023-07-18 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_translationpracticesolved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='slug',
            field=models.SlugField(allow_unicode=True, blank=True, unique=True),
        ),
    ]
