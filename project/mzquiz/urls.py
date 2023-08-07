from django.urls import path

from . import views

app_name = 'mzquiz'

urlpatterns = [
    path('', views.main, name='startpage'),
    path('detail/', views.detail, name='detail'),
    path('detail_check/', views.detail_check, name='detail_check'),
]