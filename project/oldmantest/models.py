from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class TestQuestion(models.Model):
    contents = models.TextField()
    left=models.TextField()
    right=models.TextField()

    LGX=models.IntegerField(default=0) #~1980
    RGX=models.IntegerField(default=0) #~1980

    LGY=models.IntegerField(default=0) #1981~1996
    RGY=models.IntegerField(default=0) #1981~1996

    LGMZ=models.IntegerField(default=0) #1997~
    RGMZ=models.IntegerField(default=0) #1997~

    Total=models.IntegerField(default=0) #전체 값 저장할 변수

    def __str__(self):
        return self.contents

class MZUser(models.Model):
    nickname=models.CharField(max_length=100, unique=True)
    generation=models.CharField(max_length=100)
    questions=models.JSONField(default=dict)

    def __str__(self):
        return self.nickname

    #dictionary 일차원 -> key값에는 random 문제의 번호, value에는 문제 답 여부
    # value 값에 따른 상태
    # 0-> 해당 문제의 답을 아직 선택하지 않음.
    # 1-> 해당 문제의 왼쪽 답을 선택
    # 2-> 해당 문제의 오른쪽 답을 선택

