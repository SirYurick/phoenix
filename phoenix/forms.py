from django import forms
from phoenix.models import UserProfile # , Page, Category
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    username = forms.CharField(help_text="Ваше имя")
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Ваш пароль")
    email = forms.CharField(help_text="Ваш email")
    class Meta:
        model = User
        fields = ['username', 'password', 'email', ]

class UserProfileForm(forms.ModelForm):
    website = forms.URLField(help_text="Адрес Вашего сайта", required=False)
    picture = forms.ImageField(help_text="Картинка профиля", required=False)
    class Meta:
        model = UserProfile
        fields = ['website', 'picture', ]
