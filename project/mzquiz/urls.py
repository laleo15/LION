from django.urls import path

from . import views

app_name = 'mzquiz'

urlpatterns = [
    path('detail/', views.detail, name='detail'),
]

#path('', views.main, name='startpage'),