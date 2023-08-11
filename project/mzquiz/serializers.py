from rest_framework import serializers
from .models import WordQuiz

class WordQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordQuiz
        fields = '__all__'
