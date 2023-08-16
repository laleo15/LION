from django.http import Http404
from django.shortcuts import render,redirect,get_object_or_404
from .models import WordQuiz
from django.contrib import messages
import random,json
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import WordQuizSerializer


def quiz_setting():
    #quiz question 100개 생성
    for i in range(100):
        subject="quiz"+str(i)+"번"
        answer=str(i)+"의 answer"
        wrong=str(i)+"의 wrong"

        #이미 존재하는 문제는 삽입하지 않는다.
        try:
            Q=get_object_or_404(WordQuiz,subject=subject)
        except Http404:
            q=WordQuiz(subject=subject,answer=answer, wrong=wrong)
            q.save()
    return 0

def main(request):
    # #quiz_setting()

    # random_ten=random.sample(range(50),10) #100개문제에서 random하게 10개의 문제 추출
    # #추후에 데이터베이스에는 문제 0~99번으로 등록 
    # index=0
    # count=0
    # QuizDB=WordQuiz.objects.all()
    # quiz=QuizDB[0]
    # context={
    #     'random_ten':random_ten,
    #     'index':index,
    #     'count':count,
    #     'quiz':quiz,
    #     }

    # serializer=WordQuizSerializer(context)
    # #return Response(serializer.data)
    return render(request, 'mzquiz/mainquiz.html')


@api_view(["GET","POST"])
def detail(request):

    print(request.data)

    QuizDB=WordQuiz.objects.all()
    try:
        index=int(request.data.get('index'))
        count=int(request.data.get('count'))
    except:
        random_ten=random.sample(range(50),10)
        index=0
        count=0
    else:
        data_received=request.data.get('random_ten')
        print(data_received)
        random_ten = json.loads(data_received)

    choice=request.data.get('choice')
    print("count: ",count)

    if choice=='1':
        count+=1

    print("choice: ",choice)
    print("count: ",count)
    #10문제 다 풀면 mzquiz main화면으로 화면 전환
    if index<10:
        quiz=QuizDB[random_ten[index]]
        index=index+1
    else:
        quiz=QuizDB[0]
        index=100
        #return render(request,'mzquiz/quiz_result.html',context)

    #index+1을 하는 이유는 문제 0~9로 표현하지 않고, 문제 1~10로 표현하기 위해
    context = {
        'random_ten': random_ten,
        'index': index,
        'quiz': quiz,
        'count':count,
    }

    serializer=WordQuizSerializer(context)
    return Response(serializer.data)
    #return render(request, 'mzquiz/quiz_detail.html',context)



