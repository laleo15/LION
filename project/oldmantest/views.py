from django.http import Http404
from django.shortcuts import render,redirect,get_object_or_404
from .models import MZUser
import random
# Create your views here.

def login(request):
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

    context={'user':user}
    return render(request,'oldmantest/testpage.html',context)

def update_questions(request):
    if request.method=='POST':
        nickname=request.POST.get('nickname')
        user=get_object_or_404(MZUser,nickname=nickname)

        selected_Q={}
        for key in user.questions.keys():
            selected=request.POST.get(f'group{key}')
            selected_Q[int(key)]=int(selected)

        user.questions=selected_Q
        user.save()
        context={'user':user, 'dictionary':user.questions.items()}
        
        return render(request,'oldmantest/testresult.html',context)
    return redirect('oldmantest:login')

# def test(request):
#     username=request.POST.get('username')
#     generation=request.POST.get('generation')
#     random_ten=random.sample(range(100),10) #100개문제에서 random하게 10개의 문제 추출
    
#     if generation=="none":
#         generation="세대 선택을 하지 않았습니다"
#     if username=="":
#         username="닉네임을 작성하지 않았습니다"

#     try:
#         user = User.objects.get(username=username)
#         user.questions={}
#     except User.DoesNotExist:
#         user=User(username=username, generation=generation,password=username)
    
#     #User가 있으면 받아오고, 없으면 새로 생성한다.
#     #단 원래 사용자가 있던, 없던 문제는 접속할때마다 새로운 문제를 풀 수 있게 하기 위해서 random으로 계속 갱신해준다.

#     for i in random_ten:
#         user.questions[i]=0
#     user.save()

#     context={'user':user,'random_ten':random_ten}
#     return render(request,'oldmantest/testpage.html',context)

# def update_questions(request):
#     if request.method=='POST':
#         print("username:",request)
#         user=request.user

#         for key in user.questions.keys():
#             selected=request.POST.get(f'group{key}')
#             if selected == 1:
#                 user.questions[key]=1
#             elif selected == 2:
#                 user.questions[key]=2
        
#         user.save()
#         return render(request,'oldmantest/testresult.html')
#     return redirect('oldmantest:login')

