from django.db import models

# Create your models here.

class WordQuiz(models.Model):
    subject = models.TextField()
    answer = models.TextField()
    wrong = models.TextField()
    def __str__(self):
        return self.subject