from django.urls import path
from django.views.generic import View

app_name = 'core'

from . import views

urlpatterns = [
    path('', views.home, name='login'),
]