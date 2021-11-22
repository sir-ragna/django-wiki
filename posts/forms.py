
from django import forms

class Post(forms.Form):
    title = forms.CharField(
        label="title", 
        max_length=100, 
        widget=forms.TextInput(
            attrs={'class': 'form-control mb-2', 'placeholder': 'Title'}
        )
    )
    content = forms.CharField(
        max_length=10240,
        widget=forms.Textarea(attrs={
            'class': 'form-control mb-2', 
            'rows': '10', 
            'placeholder': 'Write your article here'
        })
    )
