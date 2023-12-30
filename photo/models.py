from django.db import models
from django.utils.timezone import now


class Photo(models.Model):
    image = models.ImageField(upload_to='photo/%Y/%m/%d/')
    created = models.DateTimeField(default=now)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.image.name
# Create your models here.
