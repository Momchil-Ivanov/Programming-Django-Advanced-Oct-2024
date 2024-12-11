from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Add a comment...',
                'rows': 3,
            }),
        }


class CityForm(forms.Form):
    city = forms.CharField(max_length=100, required=False, label='Enter city')
