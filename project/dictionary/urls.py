from django.urls import path

from . import views

app_name = 'dictionary'

urlpatterns = [
    path('', views.list, name='starting'),
    path('<int:word_id>/', views.detail, name='detail'),
]