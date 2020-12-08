from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from apps.gradehoraria.mail import send_mail_template
from apps.gradehoraria.utils import generate_hash_key

from .models import PasswordReset

User = get_user_model()

class NovoUsuarioForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, label='Nome')
    last_name = forms.CharField(max_length=50, label='Sobrenome')
    email = forms.EmailField(label='E-mail')


    def clean_email(self):

        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Já existe um usuário com este e-mail')
        return email

    def save(self, commit=True):
        user = super(NovoUsuarioForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user