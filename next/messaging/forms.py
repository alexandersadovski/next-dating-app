from django import forms
from next.messaging.models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'content']
        widgets = {
            'receiver': forms.HiddenInput(),
            'content': forms.Textarea(attrs={'placeholder': 'Type a message...'}),
        }
