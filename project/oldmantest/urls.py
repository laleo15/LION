from django.urls import path

from . import views

app_name = 'oldmantest'

urlpatterns = [
    path('oldmantest/', views.main, name='page'),
]