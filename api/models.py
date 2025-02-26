from django.db import models

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