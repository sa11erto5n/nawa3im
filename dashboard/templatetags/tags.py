from django import template
from django.utils.translation import get_language
from django.utils.translation import get_language

register = template.Library()

@register.filter
def get_attr(obj, attr):
    """Get an attribute from an object dynamically."""
    return getattr(obj, attr, None)



@register.filter
def trans(value, field):
    """Returns the language-specific field value"""
    lang = get_language()
    return getattr(value, f"{field}_{lang[:2]}", "")