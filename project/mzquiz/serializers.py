from rest_framework import serializers
from .models import WordQuiz

class WordQuizSerializer(serializers.Serializer):
    index=serializers.SerializerMethodField()
    count=serializers.SerializerMethodField()
    ten_quiz=serializers.SerializerMethodField()
    
    subject = serializers.CharField(source='quiz.subject')  
    answer = serializers.CharField(source='quiz.answer')    
    wrong = serializers.CharField(source='quiz.wrong') 

    class Meta:
        model = WordQuiz
        fields = ['subject', 'answer', 'wrong','index','count','ten_quiz']


    def get_index(self, obj):
        return obj['index']

    def get_count(self,obj):
        return obj['count']
    
    def get_ten_quiz(self,obj):
        QuizDB=WordQuiz.objects.all()
        
        ten_quiz=[]
        for i in obj['random_ten']:
            quiz=QuizDB[i]
            serialized_quiz = {
                'subject': quiz.subject,
                'answer': quiz.answer,
                'wrong': quiz.wrong,
            }
            ten_quiz.append(serialized_quiz)

        return ten_quiz
