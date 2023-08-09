from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class TestQuestion(models.Model):
    contents = models.TextField()
    left=models.TextField()
    right=models.TextField()

    LGX=models.IntegerField(default=0) #~1980
    Plgx=models.IntegerField(default=0) #~1980
    RGX=models.IntegerField(default=0) #~1980
    Prgx=models.IntegerField(default=0) #~1980

    LGM=models.IntegerField(default=0) #1981~1996
    Plgm=models.IntegerField(default=0)
    RGM=models.IntegerField(default=0) #1981~1996
    Prgm=models.IntegerField(default=0)

    LGZ=models.IntegerField(default=0) #1997~
    Plgz=models.IntegerField(default=0)
    RGZ=models.IntegerField(default=0) #1997~
    Prgz=models.IntegerField(default=0)

    Total=models.IntegerField(default=0) #전체 값 저장할 변수

    def __str__(self):
        return self.contents

class MZUser(models.Model):
    nickname=models.CharField(max_length=100, unique=True)
    generation=models.CharField(max_length=100)
    questions=models.JSONField(default=dict)
    count=models.IntegerField(default=0) #사용자가 선택한 동의 개수 셀 변수

    def __str__(self):
        return self.nickname

    #dictionary 일차원 -> key값에는 random 문제의 번호, value에는 문제 답 여부
    # value 값에 따른 상태
    # 0-> 해당 문제의 답을 아직 선택하지 않음.
    # 1-> 해당 문제의 왼쪽(동의) 답을 선택
    # 2-> 해당 문제의 오른쪽(비동의) 답을 선택

class Comment(models.Model):
    nickname=models.CharField(max_length=100)
    comment=models.CharField(max_length=100)
    create_date = models.DateTimeField()

    def __str__(self):
        return self.nickname

class Grade(models.Model):
    grade=models.CharField(max_length=100)
    Fone=models.CharField(max_length=200)
    Ftwo=models.CharField(max_length=200)
    Fthird=models.CharField(max_length=200)

    def __str__(self):
        return self.grade
