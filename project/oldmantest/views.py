from django.http import Http404
from django.shortcuts import render,redirect,get_object_or_404
from .models import MZUser,TestQuestion,Comment,Grade
from django.utils import timezone
import random,json
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from .serializers import LoginSerializer ,TestSerializer,QupdateSerializer,TestQuestionSerializer



# Create your views here.

def question_setting():
    '''
    #test question 10개 생성
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
    '''
    #Grade 3개 속성 지정
    grade1="요즘꼰대"
    F1one="가르치는 것을 좋아한다."
    F1two="\"요즘 애들은~\"이라는 말을 자주 한다."
    F1third="자기 스타일을 강요한다."
    try:
        G=get_object_or_404(Grade,grade=grade1)
    except Http404:
        g=Grade(grade=grade1,Fone=F1one, Ftwo=F1two,Fthird=F1third)
        g.save()

    grade2="킹반인"
    F2one="묵직한 돌직구 표현을 선호한다."
    F2two="본인은 꼭 필요한 말만 한다고 생각한다."
    F2third="인간관계에서 선을 긋는다는 인상을 주는 경우가 많다."
    try:
        G=get_object_or_404(Grade,grade=grade2)
    except Http404:
        g=Grade(grade=grade2,Fone=F2one, Ftwo=F2two,Fthird=F2third)
        g.save()

    grade3="뼛속MZ"
    F3one="자신의 취향과 개성을 중요시하고 개인주의성향을 가진다.(누군가는 이기주의라고 한다)"
    F3two="워라벨의 영역을 분명시한다.(업무와 사생활은 뚜렷하게 구분한다, 카카오톡이 업무용으로 쓰이면 스트레스를 받는다)"
    F3third="내일보다는 오늘을, 안정보다는 리스크를 추구한다."
    try:
        G=get_object_or_404(Grade,grade=grade3)
    except Http404:
        g=Grade(grade=grade3,Fone=F3one, Ftwo=F3two,Fthird=F3third)
        g.save()
        
    return 0


#없어져도 됨
@api_view(["GET", "POST"])
def login(request):
    question_setting()
    index=0
    #추후에 데이터베이스에는 문제 0~99번으로 등록 
    context={
        'index':index,
    }
    serializer=LoginSerializer(context)
    #return Response(serializer.data)
    return render(request,'oldmantest/login.html',context)

@api_view(["GET", "POST"])
def login_after(request):
    question_setting()

    print(request.data)

    nickname=request.data.get('nickname')
    age=request.data.get('age')
    index=0
    
    #나이 -> 세대 변환
    if int(age)>=43:
        generation="X"
    elif int(age)>=27:
        generation="M"
    else:
        generation="Z"
    
    try:
        user=get_object_or_404(MZUser,nickname=nickname)
    except:
        user = MZUser.objects.create(nickname=nickname,generation=generation)

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
        'question':question,
    }
    serializer=TestSerializer(context)
    return Response(serializer.data)


@api_view(["GET", "POST"])
def test(request):

    print(request.data)

    nickname=request.data.get('nickname')
    generation=request.data.get('generation')

    index=int(request.data.get('index'))
    user=get_object_or_404(MZUser,nickname=nickname)
    
    QDB=TestQuestion.objects.all()

    try:
        selected=int(request.data.get('choice'))
    except(KeyError):
        question=QDB[index-1]
        context={
            'user':user,
            'index': index,
            'question': question,
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

        if index>=10:
            Qsetting_update(user,user.questions.items())
            return update_questions(request,user)

        question=QDB[index]

        context={
            'user':user,
            'index':index+1,
            'question':question,
        }
    serializer=TestSerializer(context)
    return Response(serializer.data)


def update_questions(request,user):
    QList=TestQuestion.objects.all()
    sendDict=[]
    selected_Q={}
    for key in user.questions.keys():
        k=int(key)
        question_data={
            "select":user.questions[key],
            "question_info":TestQuestionSerializer(QList[k]).data  
            }
        sendDict.append(question_data)
        selected_Q[int(key)]=user.questions[key]
    
    user.questions=selected_Q
    user.save()
    
    if user.count>=7:
        grade="요즘꼰대"
    elif user.count>=3:
        grade="킹반인"
    else:
        grade="뼛속MZ"
    G=get_object_or_404(Grade,grade=grade)
    
    comment_list=Comment.objects.all().order_by('-create_date')[:10]
    sendComment=[]
    date_list=[]

    for k in range(len(comment_list)):
        comment=comment_list[k]
        time = comment.create_date.strftime('%I:%M:%S %p')
        date=comment.create_date.strftime('%Y년 %m월 %d일')
        comment_data={
            'nickname':comment.nickname,
            'content':comment.comment,
            'time':time,
            'date':date
            }
        sendComment.append(comment_data)
        date_list.append(date)

    send_date=list(set(date_list))

    index=11 #결과 페이지로 넘어가라는 신호

    context={
        'index':index,
        'user':user,
        'sendDict':sendDict,
        'sendComment':sendComment,
        'date_list':send_date,
        'grade':G,
        }
    
    serializer=QupdateSerializer(context)
    return Response(serializer.data)

@api_view(["GET", "POST"])
def update_comment(request):

    print(request.data)

    nickname=request.data.get('nickname')
    generation=request.data.get('generation')

    Cnickname=nickname+'('+generation+')'
    comment=request.data.get('comment')

    create_date=timezone.now()
    
    C=Comment(nickname=Cnickname, comment=comment,create_date=create_date)
    C.save()

    user=get_object_or_404(MZUser,nickname=nickname)

    return update_questions(request,user)



def Qsetting_update(user,UserDict):
    question_list=TestQuestion.objects.all()
    user.count=0    
    for key, value in UserDict:
        q=question_list[int(key)]
        if value==1:  #left 선택
            user.count+=1
            if user.generation == "X":
                q.LGX+=1
            elif user.generation == "M":
                q.LGM+=1
            elif user.generation == "Z":
                q.LGZ+=1
        if value==2:  #right 선택
            if user.generation == "X":
                q.RGX+=1
            elif user.generation == "M":
                q.RGM+=1
            elif user.generation == "Z":
                q.RGZ+=1
        
        q.Total=q.LGX+q.RGX+q.LGM+q.RGM+q.LGZ+q.RGZ

        divX=(q.LGX+q.RGX)
        divM=(q.LGM+q.RGM)
        divZ=(q.LGZ+q.RGZ)

        if divX==0: #0으로 나눌 순 없으니까 그냥 대강 큰 수로 나누기
            divX=1000
        if divM==0:
            divM=1000
        if divZ==0:
            divZ=1000

        q.Plgx=round(q.LGX*100/divX)
        q.Plgm=round(q.LGM*100/divM)
        q.Plgz=round(q.LGZ*100/divZ)
        q.Prgx=round(q.RGX*100/divX)
        q.Prgm=round(q.RGM*100/divM)
        q.Prgz=round(q.RGZ*100/divZ)

        user.save()
        q.save()

