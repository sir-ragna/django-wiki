
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
            'placeholder': 'Write your article here',
            'style': 'font-family:monospace;'
        })
    )

class EditPost(forms.Form):
    title = forms.CharField(widget=forms.HiddenInput())
    content = forms.CharField(
        max_length=10240,
        widget=forms.Textarea(attrs={
            'class': 'form-control mb-2', 
            'rows': '25', 
            'placeholder': 'Write your article here',
            'style': 'font-family:monospace;',
        })
    )

class DeletePost(forms.Form):
    """
    Form to delete a post. We only need a hidden title form.
    """
    title = forms.CharField(widget=forms.HiddenInput())