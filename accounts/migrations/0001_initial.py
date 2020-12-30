# Generated by Django 3.1 on 2020-12-29 13:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credentials_id', models.CharField(max_length=3000)),
                ('access_token', models.CharField(max_length=3000)),
                ('access_created_at', models.DateTimeField(auto_now_add=True)),
                ('access_expires_in', models.DurationField()),
                ('refresh_token', models.CharField(max_length=100)),
                ('refresh_created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
