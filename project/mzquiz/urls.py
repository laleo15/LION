from django.urls import path

from . import views

app_name = 'mzquiz'

urlpatterns = [
    path('', views.main, name='startpage'),
    path('detail/', views.detail, name='detail'),
    path('detail_result/', views.detail_result, name='detail_result'),
]