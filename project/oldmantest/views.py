from django.shortcuts import render,redirect
from .models import MZUser
import random
# Create your views here.

def login(request):
    return render(request,'oldmantest/login.html')

def test(request):
    nickname=request.POST.get('nickname')
    generation=request.POST.get('generation')
    random_ten=random.sample(range(100),10) #100개문제에서 random하게 10개의 문제 추출
    
    if generation=="none":
        generation="세대 선택을 하지 않았습니다"
    if nickname=="":
        nickname="닉네임을 작성하지 않았습니다"
        
    user=MZUser(nickname=nickname, generation=generation)
    Userlist = MZUser.objects.all()
    if user not in Userlist:
        for i in random_ten:
            user.questions[i]=1
        user.save()

    context={'user':user,'random_ten':random_ten}
    return render(request,'oldmantest/testpage.html',context)

def update_questions(request):
    if request.method=='POST':
        #사용자가 선택한 라디오 버튼의 값을 가져옴
        selected = [request.POST.get(f'group{i}') for i in request.POST.get('random_ten')]
        print(selected)

        user.questions = selected_values
        user.save()
        
        #return redirect('quiz_result')  # 변경이 완료되면 결과 페이지로 이동
    return render(request,'oldmantest/testpage.html',context)


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
#     except User.DoesNotExist:
#         user=User(username=username, generation=generation)
#         for i in random_ten:
#             user.questions[i]=1
#         user.save()

#     context={'user':user,'random_ten':random_ten}
#     return render(request,'oldmantest/testpage.html',context)