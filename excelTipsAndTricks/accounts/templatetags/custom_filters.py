from django import template

register = template.Library()

@register.filter
def add_class(value, arg):
    if hasattr(value, 'as_widget'):
        return value.as_widget(attrs={'class': arg})
    return value  # If it's not a form field, return the value as is