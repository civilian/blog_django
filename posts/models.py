import datetime

from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    # TODO: put the required in image.
    image = models.ImageField(blank=True, null=True)
    publication_date = models.DateField()
    expiring_date = models.DateField()

    def __str__(self):
        data = {
            'title': self.title,
            'content': self.content,
            'image': self.image,
            'publication_date': self.publication_date,
            'expiring_date': self.expiring_date,
        }
        return data.__str__()
