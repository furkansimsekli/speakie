# Generated by Django 4.2.3 on 2023-07-17 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_alter_translationpractice_answer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='translationpractice',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
    ]
