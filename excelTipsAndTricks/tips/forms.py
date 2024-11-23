from django import forms
from .models import Tip
from excelTipsAndTricks.categories.models import Category
from ..tags.models import Tag


class TipForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Add tags separated by commas'}),
    )
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Tip
        fields = ['title', 'content', 'image_url', 'categories', 'tags']

    def clean_tags(self):
        tags = self.cleaned_data.get('tags', '')
        if tags:
            tags = tags.split(',')
            tag_objs = []
            for tag_name in tags:
                tag_name = tag_name.strip()
                tag_obj, created = Tag.objects.get_or_create(name=tag_name)
                tag_objs.append(tag_obj)
            return tag_objs
        return []