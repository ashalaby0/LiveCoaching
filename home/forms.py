from django import forms
from django.contrib.auth.forms import UserCreationForm

from . import models


class ClientModelForm(forms.ModelForm):
    class Meta:
        model = models.Client
        fields = ('city', 'country', 'gender', 'date_of_birth', 'photo')

        widgets = {
            'photo': forms.TextInput(attrs={
                'class':"b-none border-ccc p-10 rad-6 d-block w-full",
                'type':"file",
                'id':"pic"
                }
                ),
            'date_of_birth': forms.DateInput(attrs={
                "class":"b-none border-ccc p-10 rad-6 d-block w-full",
                "id":"date",
                "type":"date"
            }
            ),
            'gender': forms.Select(attrs={
                "id":"gender",
                "class":"form-select form-select-lg mb-3"
            }
            ),
            
        }



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
        fields = ('username', 'first_name', 'last_name', 'email', 'phone')
        widgets = {
            'first_name': forms.TextInput(attrs={
                "class" : "b-none border-ccc p-10 mt-3 rad-6 d-block w-full",
                "type":"text",
                "id":"first",
                'placeholder': 'First Name'
                }
                ),
            'last_name': forms.TextInput(attrs={
                "class" : "b-none border-ccc p-10 rad-6 d-block w-full",
                "type":"text",
                "id":"first",
                'placeholder': 'Last Name'
                }
                ),
            'phone': forms.TextInput(attrs={
                "class":"b-none border-ccc p-10 rad-6 w-full mr-10",
                "id":"number",
                "placeholder":"Phone Number"
            }),
            'email': forms.TextInput(attrs={
                "class":"b-none border-ccc p-10 mt-3 rad-6 w-full mr-10",
                "id":"email",
                "type":"email"
            }),


        }

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
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Your Name', 'class':'form-control input-lg'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email', 'class':'form-control input-lg'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone number', 'class':'form-control input-lg'}),
            'message': forms.Textarea(attrs={'placeholder': 'Your Message', "rows":"5", 'class':'form-control input-lg'})
        }
        fields = '__all__'