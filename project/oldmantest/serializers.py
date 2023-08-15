from rest_framework import serializers
from .models import TestQuestion,MZUser, Comment,Grade


class LoginSerializer(serializers.Serializer):
    index=serializers.SerializerMethodField()
    error_message=serializers.SerializerMethodField()

    def get_index(self, obj):
        return obj['index']

    def get_error_message(self,obj):
        return obj['error_message']

class TestSerializer(serializers.ModelSerializer):
    index=serializers.SerializerMethodField()
    error_message=serializers.CharField(source='error_message',default="")

    #question
    contents=serializers.CharField(source='question.contents')
    left=serializers.CharField(source='question.left')
    right=serializers.CharField(source='question.right')

    #user
    nickname=serializers.CharField(source='user.nickname')
    generation=serializers.CharField(source='user.generation')

    class Meta:
        model=MZUser,TestQuestion
        fields=[
            'contents',
            'left',
            'right',
            'nickname',
            'generation',
            'error_message',
            'index',
        ]

    def get_index(self, obj):
        return obj['index']

    def get_error_message(self,obj):
        return obj['error_message']



class QupdateSerializer(serializers.ModelSerializer):
    #문제별 세대 퍼센테이지 출력
    QuestionList=serializers.JSONField(source='sendDict')

    #실시간 10개 Comment 리스트 출력
    CommentList=serializers.JSONField(source='sendComment')

    #실시간 comment에 있는 list 출력
    date_list=serializers.JSONField(source='date_list')

    #user
    nickname=serializers.CharField(source='user.nickname')
    generation=serializers.CharField(source='user.generation')

    #Grade
    grade=serializers.CharField(source='G')

    class Meta:
        model=MZUser,Grade,Comment
        fields=[
            'nickname',
            'generation',
            'QuestionList',
            'CommentList',
            'grade',
        ]
