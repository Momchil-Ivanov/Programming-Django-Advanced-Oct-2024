from django import forms
from .models import Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'image_url', 'tags']
        widgets = {
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        category = self.instance

        if Category.objects.filter(name=name).exclude(id=category.id).exists():
            raise forms.ValidationError("A category with this name already exists.")
        return name
