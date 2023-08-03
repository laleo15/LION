from django.shortcuts import render

# Create your views here.

def test(request):
    return render(request,'oldmantest/testpage.html')

def login(request):
    return render(request,'oldmantest/login.html')