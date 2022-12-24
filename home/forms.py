from django import forms
from django.contrib.auth.forms import UserCreationForm

from . import models


class ClientModelForm(forms.ModelForm):
    class Meta:
        model = models.Client
        fields = '__all__'


class CoachModelForm(forms.ModelForm):
    class Meta:
        model = models.Coach
        fields = '__all__'


class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = models.Category
        fields = '__all__'


class SessionModelForm(forms.ModelForm):
    class Meta:
        model = models.Session
        widgets = {
            'time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'})
        }
        fields = '__all__'


class UserModelForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = '__all__'


class SignUpForm(UserCreationForm):
    class Meta:
        model=models.User
        fields=('username','email','password1','password2', 'phone')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone number'})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': 'Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': 'Password (again)'})





class CustomerMessageForm(forms.ModelForm):
    class Meta:
        model = models.CustomerMessage
        fields = '__all__'