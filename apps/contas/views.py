from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from django.contrib import messages
from django.contrib.auth.forms import (PasswordChangeForm, PasswordResetForm, SetPasswordForm)
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import User

from .forms import NovoUsuarioForm


@login_required(login_url='/contas/login')
def novo_usuario(request):
    template_name = 'novo-usuario.html'
    if request.method == 'POST':
        form = NovoUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário cadastrado com sucesso!')
            return redirect('novo_usuario')
        else:
            messages.warning(request, 'Por favor, corrija os erros abaixo!')
    else:
        form = NovoUsuarioForm()
    context = {
        'form': form
    }
    return render(request, template_name, context)


def login_usuario(request):
    tempate_name = 'login_usuario.html'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET.get('next', '/'))
        else:
            messages.error(request, 'Usuário ou senha inválido')
    return render(request, tempate_name)


@login_required(login_url='/contas/login')
def logout_usuario(request):
    logout(request)
    return redirect('contas:login_usuario')


@login_required(login_url='/contas/login')
def alterar_senha(request):
    template_name = 'alterar_senha.html'
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Senha alterada com sucesso!')
            return redirect('contas:alterar_senha')
        else:
            messages.error(request, 'Não foi possível alterar a senha. Por favor, corrija os erros e tente novamente')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form
    }
    return render(request, template_name, context)
