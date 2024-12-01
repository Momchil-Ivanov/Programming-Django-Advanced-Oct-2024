from django import forms
from .models import Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'image_url']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        # Get the current category object (if updating an existing one)
        category = self.instance

        # Check if a category with the same name already exists and it is not the current category
        if Category.objects.filter(name=name).exclude(id=category.id).exists():
            raise forms.ValidationError("A category with this name already exists.")
        return name