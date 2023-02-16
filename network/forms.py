from django import forms

class NewPostForm(forms.Form):
    
    body = forms.CharField(label='New Post', max_length=400, widget=forms.Textarea(attrs={
        'placeholder': 'Write a new post!',
        'rows': 5,
        'class': 'form-control form-control-sm'
    }))
