# templatetags/form_tags.py
from django import template

register = template.Library()

@register.filter
def add_class(field, css_class):
    """
    This filter will add a CSS class to a field.
    """
    return field.as_widget(attrs={'class': css_class})

