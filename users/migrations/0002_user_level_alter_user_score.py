# Generated by Django 4.2.3 on 2023-07-18 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='level',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='score',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
