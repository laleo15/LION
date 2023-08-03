from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class TestQuestion(models.Model):
    subject = models.TextField()
    GX=models.IntegerField() #~1980
    GY=models.IntegerField() #1981~1996
    GMZ=models.IntegerField() #1997~
    def __str__(self):
        return self.subject

class User(AbstractUser):
    nickname=models.CharField(max_length=100)
    generation=models.CharField(max_length=100)
