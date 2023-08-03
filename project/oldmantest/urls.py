from django.urls import path

from . import views

app_name = 'oldmantest'

urlpatterns = [
    path('', views.login, name='login'),
    path('test',views.test,name='test'),
    path('test/update_questions',views.update_questions,name='update_questions'),
]