from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth import authenticate, login
# from django.contrib.auth.models import User

def start(request):
    return render(request, 'common/main.html') 

def menu(request):
    return render(request, 'common/menu.html') 


