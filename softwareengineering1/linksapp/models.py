from django.db import models

# Create your models here.
class Links(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title
