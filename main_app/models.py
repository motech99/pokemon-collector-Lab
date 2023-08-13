from django.db import models

# Create your models here.
class Pokemon(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    description = models.TextField(max_length=100)
    age = models.IntegerField()



