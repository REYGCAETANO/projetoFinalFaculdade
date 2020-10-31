from django.conf.urls import url

from . import views

app_name = 'contas'

urlpatterns = [
    url('novo_usuario/', views.novo_usuario, name='novo_usuario'),
    url('login/', views.login_usuario, name='login_usuario'),
    url('logout/', views.logout_usuario, name='logout_usuario'),
    url('alterar-senha/', views.alterar_senha, name='alterar_senha'),

]
