from django.urls import path

from . import views

app_name = 'mzquiz'

urlpatterns = [
    path('', views.main, name='startpage'),
    path('detail/', views.detail, name='detail'),
    prth('result/',views.result, name='result')
]