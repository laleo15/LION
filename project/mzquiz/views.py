from django.http import Http404
from django.shortcuts import render,redirect,get_object_or_404
from .models import WordQuiz
from django.contrib import messages
import random,json
from .forms import RadioForm
# Create your views here.

def quiz_setting():
    #quiz question 100개 생성
    quiz_list=[]
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
            quiz_list.append(q)
    return 0


def main(request):
    quiz_setting()

    random_ten=random.sample(range(100),10) #100개문제에서 random하게 10개의 문제 추출
    #추후에 데이터베이스에는 문제 0~99번으로 등록 
    index=0

    context={'random_ten':random_ten,'index':index}

    return render(request, 'mzquiz/mainquiz.html',context)


def detail(request):
    QuizDB=WordQuiz.objects.all()
    data_received=request.POST.get('random_ten')
    index=int(request.POST.get('index'))
    
    random_ten = json.loads(data_received)
    quiz=QuizDB[random_ten[index]]

    form = RadioForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            group_value = form.cleaned_data['group']
            if group_value == '1':
                messages.success(request, "answer!")
            else:
                messages.error(request, "wrong!")

    context = {
        'random_ten': random_ten,
        'index': index,
        'quiz': quiz,
        'form': form,
    }

    return render(request, 'mzquiz/quiz_detail.html',context)


def detail_check(request):
    QuizDB=WordQuiz.objects.all()
    data_received=request.POST.get('random_ten')
    random_ten = json.loads(data_received)
    index=int(request.POST.get('index'))+1

    #10문제 다 풀면 mzquiz main화면으로 화면 전환
    if index==10:
        return redirect('mzquiz:startpage')

    quiz=QuizDB[random_ten[index]]

    form = RadioForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            group_value = form.cleaned_data['group']
            if group_value == '1':
                messages.success(request, "answer!")
            else:
                messages.error(request, "wrong!")


    context = {
        'random_ten': random_ten,
        'index': index,
        'quiz': quiz,
        'form': form,
    }

    return render(request, 'mzquiz/quiz_detail.html',context)