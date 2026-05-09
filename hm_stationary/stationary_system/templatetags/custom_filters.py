# myapp/templatetags/custom_filters.py
from django import template
import os

register = template.Library()

@register.filter
def basename(value):
    """Return just the file name from a file path."""
    return os.path.basename(value)

@register.filter
def endswith(value, arg):
    return str(value).lower().endswith(str(arg).lower())