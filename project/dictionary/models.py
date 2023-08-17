from django.db import models

# Create your models here.

class Word(models.Model):
    subject = models.CharField(max_length=200)
    meaning = models.TextField()
    generation = models.CharField(max_length=100)
    origin=models.TextField()
    standard = models.CharField(max_length=200)
    count=models.IntegerField(default=0)
    url=models.TextField()
    
    def __str__(self):
        return str(self.subject)
    
class Synonym(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    synonym = models.CharField(max_length=200,default="유의어가 존재하지 않습니다..")
    
    def __str__(self):
        return str(self.word)
    
class Example(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    example = models.TextField(default="해당 단어를 문장으로 만들 수 없습니다..")
    
    def __str__(self):
        return str(self.word)