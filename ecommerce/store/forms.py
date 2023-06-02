from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm,SetPasswordForm
from django.contrib.auth.models import User
from .models import Customer
from django.core.exceptions import ValidationError



class LoginForm(AuthenticationForm):
    username = UsernameField(label='Ваше Имя:',widget=forms.TextInput(attrs={'autofocus':'True', 'class':'form-control'}))
    password = forms.CharField(label='Пароль',widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))

class CustomerRegistrationForm(UserCreationForm):
    username = forms.CharField(label='Введите ваше Имя:',required=True,widget=forms.TextInput(attrs={'autofocus':'True', 'class':'form-control'}))
    email = forms.EmailField(label='Введите вашу электронная почту:',required=True,widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='Введите пароль:',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label = 'Подтвердите пароля:', widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


    

        


    




class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Старый пароль', widget=forms.PasswordInput(attrs={'autofocus':'True', 'autocomplete':'current-password', 'class':'form-control'}))
    new_password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))
    new_password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control' }))


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label='Ваша электронная почта',widget=forms.EmailInput(attrs={'autofocus':True, 'autocomplete':'current-email', 'class':'form-control'}))

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))
    new_password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control' }))


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['адрес','имя','город','страна','почтовый_индекс', 'номер_телефона']
        widgets = {'имя':forms.TextInput(attrs={'class':'form-control'}),
                   'адрес':forms.TextInput(attrs={'class':'form-control'}),
                   'город':forms.TextInput(attrs={'class':'form-control'}),
                   'страна':forms.Select(attrs={'class':'form-control'}),
                   'почтовый_индекс':forms.NumberInput(attrs={'class':'form-control'}),
                   'номер_телефона':forms.NumberInput(attrs={'class':'form-control'}),
                   }

