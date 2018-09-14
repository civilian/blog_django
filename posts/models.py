import datetime

from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(blank=True, null=True)
    publication_date = models.DateField(default=datetime.date.today)
    expiring_date = models.DateField()

    def __str__(self):
        return self.image.__str__()
