from django import forms
from .models import WhatsAppBot, Trigger

class WhatsAppBotForm(forms.ModelForm):
    class Meta:
        model = WhatsAppBot
        fields = ['name', 'phone_number', 'token', 'webhook_url']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'token': forms.PasswordInput(attrs={'class': 'form-control'}),
            'webhook_url': forms.URLInput(attrs={'class': 'form-control'}),
        }


class TriggerForm(forms.ModelForm):
    class Meta:
        model = Trigger
        fields = ['keyword', 'response']
        widgets = {
            'keyword': forms.TextInput(attrs={'class': 'form-control'}),
            'response': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
