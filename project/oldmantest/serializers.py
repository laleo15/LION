from rest_framework import serializers
from .models import TestQuestion,MZUser, Comment,Grade

class MZUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MZUser
        fields ='__all__'

class TestQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestQuestion
        fields = ['contents', 'left', 'right']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields='__all__'


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Grade
        fields='__all__'

class LoginSerializer(serializers.Serializer):
    index=serializers.SerializerMethodField()

    def get_index(self, obj):
        return obj['index']


class TestSerializer(serializers.Serializer):
    index=serializers.SerializerMethodField()

    #question
    question=TestQuestionSerializer()

    #user
    user=MZUserSerializer() 

    class Meta:
        fields=[
            'question',
            'user'
            'error_message',
            'index',
        ]

    def get_index(self, obj):
        return obj['index']


class QupdateSerializer(serializers.Serializer):
    #문제별 세대 퍼센테이지 출력
    QuestionList=serializers.SerializerMethodField()

    #실시간 10개 Comment 리스트 출력
    CommentList=serializers.SerializerMethodField()

    #실시간 comment에 있는 list 출력
    date_list=serializers.SerializerMethodField()

    #user
    user=MZUserSerializer()

    #Grade
    grade=GradeSerializer()

    class Meta:
        fields=[
            'user'
            'date_list',
            'QuestionList',
            'CommentList',
            'grade',
        ]

    def get_QuestionList(self,obj):
        return obj['sendDict']
    
    def get_CommentList(self, obj):
        
        return obj['sendComment']

    
    def get_date_list(self,obj):
        return obj['date_list']
