from django.db import models
from accounts.models import Item

class HomePage(models.Model):
    featured_items = models.ManyToManyField(Item)

    def __str__(self):
        return "Home Page"