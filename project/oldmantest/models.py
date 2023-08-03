from django.db import models

# Create your models here.

class TestQuestion(models.Model):
    subject = models.TextField()

    def __str__(self):
        return self.subject

class Userdata(models.Model):
    user=models.CharField(max_length=100)