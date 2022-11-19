from django.forms import ModelForm

from . import models


class ClientModelForm(ModelForm):
    class Meta:
        model = models.Client
        fields = '__all__'


class CoachModelForm(ModelForm):
    class Meta:
        model = models.Coach
        fields = '__all__'


class CategoryModelForm(ModelForm):
    class Meta:
        model = models.Category
        fields = '__all__'


class SessionModelForm(ModelForm):
    class Meta:
        model = models.Session
        fields = '__all__'


class UserModelForm(ModelForm):
    class Meta:
        model = models.User
        fields = '__all__'
