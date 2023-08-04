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

class MZUser(models.Model):
    nickname=models.CharField(max_length=100, unique=True)
    generation=models.CharField(max_length=100)
    questions=models.JSONField(default=dict)

    def __str__(self):
        return self.nickname

    #dictionary 일차원 -> key값에는 random 문제의 번호, value에는 문제 답 여부
    # value 값에 따른 상태
    # 0-> 해당 문제의 답을 아직 선택하지 않음.
    # 0-> 해당 문제의 왼쪽 답을 선택
    # 1-> 해당 문제의 오른쪽 답을 선택

    #list 일차원 배열-> 0이면 해당 인덱스 번호 풀지 않은 것,
    # 0이 아니면 해당 인덱스 번호를 푼 것.
    # 1-> 해당 문제의 왼쪽 답을 선택
    # 2-> 해당 문제의 오른쪽 답을 선택

# class User(AbstractUser):
#     #nickname=models.CharField(max_length=100)
#     generation=models.CharField(max_length=100)
#     questions=models.JSONField(default=[0]*100)

#     def __str__(self):
#         return self.username

