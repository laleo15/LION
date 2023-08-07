from django.http import Http404
from django.shortcuts import render,redirect,get_object_or_404
from .models import MZUser,TestQuestion
import random
from .forms import AnswerForm

# Create your views here.

def question_setting():
    #test question 100개 생성
    question_list=[]
    for i in range(100):
        contents="test"+str(i)+"번"
        left=str(i)+"의 left"
        right=str(i)+"의 right"

        #이미 존재하는 문제는 삽입하지 않는다.
        try:
            Q=get_object_or_404(TestQuestion,contents=contents)
        except Http404:
            q=TestQuestion(contents=contents,left=left, right=right)
            q.save()
            question_list.append(q)
        
    return 0

def Qsetting_update(user,UserDict):
    question_list=TestQuestion.objects.all()    

    for key, value in UserDict:
        q=question_list[key]
        if value==1:
            if user.generation == "X세대":
                q.LGX+=1
            elif user.generation == "Y세대":
                q.LGY+=1
            elif user.generation == "MZ세대":
                q.LGMZ+=1
        if value==2:
            print(user.generation)
            if user.generation == "X세대":
                q.RGX+=1
            elif user.generation == "Y세대":
                q.RGY+=1
            elif user.generation == "MZ세대":
                q.RGMZ+=1
        q.Total=q.LGX+q.RGX+q.LGY+q.RGY+q.LGMZ+q.RGMZ
        q.save()

def login(request):
    question_setting()
    return render(request,'oldmantest/login.html')

def test(request):
    nickname=request.POST.get('nickname')
    generation=request.POST.get('generation')
    random_ten=random.sample(range(100),10) #100개문제에서 random하게 10개의 문제 추출
    #추후에 데이터베이스에는 문제 0~99번으로 등록 
    
    if generation=="none":
        generation="세대 선택을 하지 않았습니다"
    if nickname=="":
        nickname="닉네임을 작성하지 않았습니다"
        
    try:
        user=get_object_or_404(MZUser,nickname=nickname)
        user.questions={}
    except Http404:
        user=MZUser(nickname=nickname,generation=generation)
    
    #User가 있으면 받아오고, 없으면 새로 생성한다.
    #단 원래 사용자가 있던, 없던 문제는 접속할때마다 새로운 문제를 풀 수 있게 하기 위해서 random으로 계속 갱신해준다.

    for i in random_ten:
        user.questions[i]=0
    user.save()

    form=AnswerForm(request.POST, questions=user.questions)
    if form.is_valid():
        pass
    else:
        form = AnswerForm(questions=user.questions)

    context={'user':user,'form':form}
    return render(request,'oldmantest/testpage.html',context)

def update_questions(request):
    if request.method=='POST':
        nickname=request.POST.get('nickname')
        user=get_object_or_404(MZUser,nickname=nickname)

        selected_Q={}
        for key in user.questions.keys():
            selected=request.POST.get(f'question_{key}')
            selected_Q[int(key)]=int(selected)

        user.questions=selected_Q
        user.save()

        Qsetting_update(user,user.questions.items())
        QList=TestQuestion.objects.all()
        
        sendDict={}
        for key in user.questions.keys():
            sendDict[key]=[user.questions[key],QList[key]]

        
        context={'user':user, 'sendDict':sendDict.items()}
        
        return render(request,'oldmantest/testresult.html',context)
    return redirect('oldmantest:login')
