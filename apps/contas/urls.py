from django.conf.urls import url
from django.urls import path
from django.contrib.auth import urls
from django.contrib.auth import views as auth_views

from . import views

app_name = 'contas'

urlpatterns = [
    path('novo_usuario/', views.novo_usuario, name='novo_usuario'),
    path('login/', views.login_usuario, name='login_usuario'),
    path('logout/', views.logout_usuario, name='logout_usuario'),
    path('alterar-senha/', views.alterar_senha, name='alterar_senha'),



    # url('reset-senha-confirmacao/<key>\w+)/$', views.reset_senha_confirmacao, name='reset_senha_confirmacao'),

]