from django.forms import ModelForm

from . import models

class ClientModelForm(ModelForm):
    class Meta:
        model = models.Client

class CoachModelForm(ModelForm):
    class Meta:
        model = models.Coach

class CategoryModelForm(ModelForm):
    class Meta:
        model = models.Category


class SessionModelForm(ModelForm):
    class Meta:
        model = models.Session

class UserModelForm(ModelForm):
    class Meta:
        model = models.User

