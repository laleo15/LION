from django.shortcuts import render

# Create your views here.

def main(request):
    return render(request, 'oldmantest/login.html') 

def test(request):
    return render(request,'oldmantest/testpage.html')