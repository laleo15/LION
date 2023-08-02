from django.urls import path

from . import views

app_name = 'mzquiz'

urlpatterns = [
    path('mzquiz', views.main, name='startpage'),
]