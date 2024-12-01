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
        tags = self.cleaned_data.get('tags', '').strip()
        if tags:
            tag_objs = []
            tag_names = tags.split(',')
            for tag_name in tag_names:
                tag_name = tag_name.strip()
                if tag_name:  # Ensure no empty tags are processed
                    tag_obj, created = Tag.objects.get_or_create(name=tag_name)
                    tag_objs.append(tag_obj)
            return tag_objs
        return []

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if self.instance.pk:
            # If editing, exclude the current tip
            if Tip.objects.exclude(pk=self.instance.pk).filter(title=title).exists():
                raise forms.ValidationError("A tip with this title already exists.")
        else:
            # If creating a new tip, check if the title already exists
            if Tip.objects.filter(title=title).exists():
                raise forms.ValidationError("A tip with this title already exists.")
        return title