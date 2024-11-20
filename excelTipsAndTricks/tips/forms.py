from django import forms
from .models import Tip

class TipForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Add tags separated by commas'}),
    )

    class Meta:
        model = Tip
        fields = ['title', 'content']  # Add other fields as needed