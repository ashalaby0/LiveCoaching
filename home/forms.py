from django import forms

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
