from django import forms
from .models import Comment

class CommentModelForm(forms.ModelForm):
    content = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Add a comment'})
    )

    class Meta:
        model = Comment
        fields = ['content']
