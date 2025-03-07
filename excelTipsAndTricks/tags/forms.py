from django import forms
from excelTipsAndTricks.tags.models import Tag

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data['name'].strip().lower()

        if not name:
            raise forms.ValidationError('Tag name cannot be empty.')

        if len(name) > 50:
            raise forms.ValidationError('Tag name is too long. Max length is 50 characters.')

        return name
