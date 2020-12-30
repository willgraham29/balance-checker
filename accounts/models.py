from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Token(models.Model):
    credentials_id = models.CharField(max_length=3000)
    access_token = models.CharField(max_length=3000)
    access_created_at = models.DateTimeField(auto_now_add=True)
    access_updated_at = models.DateTimeField(auto_now=True)
    access_expires_in = models.DurationField()
    refresh_token = models.CharField(max_length=100)
    refresh_created_at = models.DateTimeField(auto_now_add=True)
    refresh_updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
