from django import forms
from .models import Tip
from excelTipsAndTricks.categories.models import Category
from ..tags.models import Tag


class TipForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2-multiple'})
    )

    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all().order_by('name'),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Tip
        fields = ['title', 'content', 'image_url', 'tags', 'categories']

    def clean_tags(self):
        tags = self.cleaned_data.get('tags', [])
        tag_names = [tag.name.lower() for tag in tags]

        if len(tag_names) != len(set(tag_names)):
            raise forms.ValidationError("Duplicate tags are not allowed.")

        return tags

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if self.instance.pk:
            if Tip.objects.exclude(pk=self.instance.pk).filter(title=title).exists():
                raise forms.ValidationError("A tip with this title already exists.")
        else:
            if Tip.objects.filter(title=title).exists():
                raise forms.ValidationError("A tip with this title already exists.")
        return title
