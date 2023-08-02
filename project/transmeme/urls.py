from django.urls import path

from . import views

app_name = 'transmeme'

urlpatterns = [
    path('transmeme/', views.main, name='translator'),
]