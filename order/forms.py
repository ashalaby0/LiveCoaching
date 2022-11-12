from django import forms

from . import models

class PaymentModelForm(forms.ModelForm):
    class Meta:
        model = models.Payment
        fields = '__all__'
         