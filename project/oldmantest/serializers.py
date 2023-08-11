from rest_framework import serializers
from .models import TestQuestion,MZUser, Comment,Grade

class TestQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestQuestion
        fields = '__all__'

class MZUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MZUser
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'
