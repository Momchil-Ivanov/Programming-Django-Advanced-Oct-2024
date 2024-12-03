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
        widget=forms.CheckboxSelectMultiple,  # Use a multiple select box for categories
    )

    class Meta:
        model = Tip
        fields = ['title', 'content', 'image_url', 'tags', 'categories']

    def clean_tags(self):
        tags = self.cleaned_data.get('tags', [])
        tag_names = [tag.name.lower() for tag in tags]

        # Ensure no duplicate tags in the list (case-insensitive)
        if len(tag_names) != len(set(tag_names)):
            raise forms.ValidationError("Duplicate tags are not allowed.")

        return tags

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_categories = self.object.categories.all()  # QuerySet of selected categories
        selected_category_ids = selected_categories.values_list('id', flat=True)  # List of selected category IDs
        context['selected_categories'] = selected_categories  # Full category objects
        context['selected_category_ids'] = selected_category_ids  # List of selected category IDs for filtering
        return context