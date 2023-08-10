from django.urls import path

from . import views

app_name = 'dictionary'

urlpatterns = [
    path('all/', views.list, name='starting'),
    path('generation/', views.list1, name='generation'),
    path('<int:word_id>/', views.detail, name='detail'),
]