from django.db import models
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
    return f'user_{instance.user.id}/{filename}'

# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='blog_images/')
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    about = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)

    def __str__(self):
        return self.user.username