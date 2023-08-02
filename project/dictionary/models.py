from django.db import models

# Create your models here.

class Word(models.Model):
    subject = models.CharField(max_length=200)
    generation = models.TextField()

    def __str__(self):
        return self.subject

class Meaning(models.Model): 
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    content = models.TextField()
    origin=models.TextField()