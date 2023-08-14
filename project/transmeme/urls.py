from django.urls import path

from . import views

app_name = 'transmeme'

urlpatterns = [
    path('', views.main, name='translator'),
    path('translate/', views.translate, name='translate'),
    path('apitest/', views.translate1),
]
