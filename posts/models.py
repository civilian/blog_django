from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField()
    publication_date = models.DateField()
    expiring_date = models.DateField()
