from django import forms
from django.contrib.auth.forms import UserCreationForm

from . import models


class ClientModelForm(forms.ModelForm):
    class Meta:
        model = models.Client
        fields = ('photo', )
        widgets = {
            'photo': forms.TextInput(attrs={
                'class':"b-none border-ccc p-10 rad-6 d-block w-full",
                'type':"file",
                'id':"pic"
                }
                ),
        }

class CoachModelForm(forms.ModelForm):
    class Meta:
        model = models.Coach
        fields = ('category', 'price_per_hour','price_per_30_mins', 'available_for_kids', 'working_hours_start', 'working_hours_end', 'bio', 'photo')


        widgets = {
            'photo': forms.TextInput(attrs={
                'class':"b-none border-ccc p-10 rad-6 d-block w-full",
                'type':"file",
                'id':"pic"
                }
                ),
            'category': forms.TextInput(attrs={
                "class":"b-none border-ccc p-10 rad-6 d-block w-full",
                "type":"text"
            }
            ),
            'price_per_hour': forms.TextInput(attrs={
                "type":"number",
                "class":"form-control mb-3 w-100"
            }
            ),
            'price_per_30_mins': forms.TextInput(attrs={
                "type":"number",
                "class":"form-control mb-3 w-100"
            }
            ),
            'available_for_kids': forms.TextInput(attrs={
                "class":"btn-check mb-3 w-100"
            }
            ),
            'working_hours_start': forms.TimeInput(attrs={
                'type':'time',
                "class":"form-control mb-3 w-100"
            }),
            'working_hours_end': forms.TimeInput(attrs={
                'type':'time',
                "class":"form-control mb-3 w-100"
            }),
            'bio': forms.Textarea(attrs={
                'class':"form-control mb-3 w-100"
            })
        }



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
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'city', 'country', 'gender', 'date_of_birth')
        widgets = {
            'username': forms.TextInput(attrs={
                "class" : "b-none border-ccc p-10 mt-3 rad-6 d-block w-full",
                "type":"text",
                "id":"first",
                'placeholder': 'User Name'
                }
                ),
            'city': forms.TextInput(attrs={
                "class" : "b-none border-ccc p-10 mt-3 rad-6 d-block w-full",
                "type":"text",
                "id":"first",
                'placeholder': 'City'
                }
                ),
            'country': forms.TextInput(attrs={
                "class" : "b-none border-ccc p-10 mt-3 rad-6 d-block w-full",
                "type":"text",
                "id":"first",
                'placeholder': 'Country'
                }
                ),
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
            
            'email': forms.TextInput(attrs={
                "class":"b-none border-ccc p-10 mt-3 rad-6 w-full mr-10",
                "id":"email",
                "type":"email"
            }),
            'phone': forms.TextInput(attrs={
                "class":"b-none border-ccc p-10 rad-6 w-full mr-10",
                "id":"number",
                "placeholder":"Phone Number"
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
                "class":"form-select form-select-lg mb-3 d-block w-100"
            }
            ),


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


class CertificateForm(forms.ModelForm):
    class Meta:
        model = models.Certificate
        fields = '__all__'
        