# Generated by Django 4.2.3 on 2023-07-11 08:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Moderator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(default='')),
                ('profile_picture', models.ImageField(default='default_profile_pic.jpg ', upload_to='profile_pictures/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.PositiveIntegerField(default=0)),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
            ],
        ),
        migrations.RemoveField(
            model_name='studentprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='ModeratorProfile',
        ),
        migrations.DeleteModel(
            name='StudentProfile',
        ),
        migrations.AddField(
            model_name='moderator',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.profile'),
        ),
    ]
