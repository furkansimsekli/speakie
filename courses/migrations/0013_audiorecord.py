# Generated by Django 4.2.3 on 2023-07-27 09:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0012_alter_speakingpractice_title_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AudioRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audio_file', models.FileField(upload_to='')),
                ('practice', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='courses.speakingpractice')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]