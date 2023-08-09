from django.http import Http404
from django.shortcuts import render,redirect,get_object_or_404
from .models import MZUser,TestQuestion,Comment
from django.utils import timezone
import random,json

# Create your views here.

def question_setting():
    #test question 10개 생성
    question_list=[]
    for i in range(10):
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


def login(request):
    question_setting()
    index=0
    #추후에 데이터베이스에는 문제 0~99번으로 등록 
    context={
        'index':index
    }
    return render(request,'oldmantest/login.html',context)

def login_after(request):
    nickname=request.POST.get('nickname')
    generation=request.POST.get('generation')
    index=int(request.POST.get('index'))
    
    #예외처리
    if nickname=="":
        error_message="닉네임을 작성하지 않았습니다"
        context={
            'index':index,
            'error_message':error_message
        }
        return render(request,"oldmantest/login.html",context)

    if generation=="none":
        error_message="세대 선택을 하지 않았습니다"
        context={
            'index':index,
            'error_message':error_message
        }
        return render(request,"oldmantest/login.html",context)
        

    try:
        user=get_object_or_404(MZUser,nickname=nickname)
        user.questions={}
        if user.generation!=generation:
            error_message="이미 존재하는 닉네임입니다!"
            context={
                'index':index,
                'error_message':error_message
            }
            return render(request,"oldmantest/login.html",context)
    except Http404:
        user=MZUser(nickname=nickname,generation=generation)
    
    #User가 있으면 받아오고, 없으면 새로 생성한다.
    #단 원래 사용자가 있던, 없던 문제는 접속할때마다 새로운 문제를 풀 수 있게 하기 위해서 random으로 계속 갱신해준다.

    for i in range(10):
        user.questions[i]=0
    user.save()

    QDB=TestQuestion.objects.all()
    question=QDB[index]

    context={
        'user':user,
        'index':index+1,
        'question':question
    }

    return render(request,'oldmantest/testpage.html',context)



def test(request):
    nickname=request.POST.get('nickname')
    generation=request.POST.get('generation')
    data_received=request.POST.get('random_ten')

    index=int(request.POST.get('index'))
    user=get_object_or_404(MZUser,nickname=nickname)
    
    QDB=TestQuestion.objects.all()

    try:
        selected=int(request.POST['choice'])
    except(KeyError):
        question=QDB[index-1]
        context={
            'user':user,
            'index': index,
            'question': question,
            'error_message':"You didn't select a choice"
        }
    else:
        selected_Q={}
        for key in user.questions.keys():
            if int(key)==index-1:
                selected_Q[int(key)]=selected
            else:
                selected_Q[int(key)]=user.questions[key]

        user.questions=selected_Q
        user.save()

        if index==10:
            return update_questions(request,user)

        question=QDB[index]

        context={
            'user':user,
            'index':index+1,
            'question':question
        }
    return render(request,'oldmantest/testpage.html',context)



def Qsetting_update(user,UserDict):
    question_list=TestQuestion.objects.all()    

    for key, value in UserDict:
        q=question_list[int(key)]
        if value==1:  #left 선택
            if user.generation == "X세대":
                q.LGX+=1
            elif user.generation == "M세대":
                q.LGM+=1
            elif user.generation == "Z세대":
                q.LGZ+=1
        if value==2:  #right 선택
            if user.generation == "X세대":
                q.RGX+=1
            elif user.generation == "M세대":
                q.RGM+=1
            elif user.generation == "Z세대":
                q.RGZ+=1
        
        q.Total=q.LGX+q.RGX+q.LGM+q.RGM+q.LGZ+q.RGZ

        q.Plgx=round(q.LGX*100/q.Total)
        q.Plgm=round(q.LGM*100/q.Total)
        q.Plgz=round(q.LGZ*100/q.Total)
        q.Prgx=round(q.RGX*100/q.Total)
        q.Prgm=round(q.RGM*100/q.Total)
        q.Prgz=round(q.RGZ*100/q.Total)
        q.save()



def update_questions(request,user):
    Qsetting_update(user,user.questions.items())
    QList=TestQuestion.objects.all()
    sendDict={}
    
    for key in user.questions.keys():
        k=int(key)
        sendDict[k]=[user.questions[key],QList[k]]

    comment_list=Comment.objects.order_by('-create_date')[:10]
    context={
        'user':user,
        'sendDict':sendDict.items(),
        'comment_list':comment_list,
        }
    
    return render(request,'oldmantest/testresult.html',context)

    

def update_comment(request):
    nickname=request.POST.get('nickname')
    generation=request.POST.get('generation')

    Cnickname=nickname+'('+generation[0]+')'
    comment=request.POST.get('comment')
    create_date=timezone.now()
    
    C=Comment(nickname=Cnickname, comment=comment,create_date=create_date)
    C.save()

    comment_list=Comment.objects.order_by('-create_date')[:10]
    user=get_object_or_404(MZUser,nickname=nickname)
    
    QList=TestQuestion.objects.all()
    sendDict={}
    for key in user.questions.keys():
        k=int(key)
        sendDict[k]=[user.questions[key],QList[k]]
    
    context={
        'user':user,
        'sendDict':sendDict.items(),
        'comment_list':comment_list,
        }

    return render(request,'oldmantest/testresult.html',context)

