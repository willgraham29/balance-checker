# Generated by Django 3.1 on 2020-12-29 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='access_updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='token',
            name='refresh_updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
