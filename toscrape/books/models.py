from django.db import models


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=250)
    price = models.FloatField()
    description = models.TextField()
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
