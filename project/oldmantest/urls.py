from django.urls import path

from . import views
from django.contrib.auth import views as auth_views


app_name = 'oldmantest'

urlpatterns = [
    path('', views.login, name='login'),
    path('/login_after',views.login_after,name='login_after'),
    path('test',views.test,name='test'),
    path('test/update_questions',views.update_questions,name='update_questions'),
    path('test/update_comment',views.update_comment,name='update_comment'),
]