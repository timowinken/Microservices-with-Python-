from django.db import models

# Django-Model, um Daten in Datenbank zu speichern und abzurufen
class Product(models.Model):
    title = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    likes = models.PositiveIntegerField(default=0)

class User(models.Model):
    pass