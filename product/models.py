from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.CharField(max_length=20)
    image_url = models.URLField(max_length=500)

    def __str__(self):
        return self.title
