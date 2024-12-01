from django import forms
from .models import Tip
from excelTipsAndTricks.categories.models import Category
from ..tags.models import Tag

class TipForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Add tags separated by commas'}),
    )

    # Categories should still be a ModelMultipleChoiceField, but it won't show as a select box
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all().order_by('name'),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),  # Use a multiple select box for categories
    )

    class Meta:
        model = Tip
        fields = ['title', 'content', 'image_url', 'tags', 'categories']

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
