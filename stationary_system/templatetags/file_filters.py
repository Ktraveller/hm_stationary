from django import template

register = template.Library()

@register.filter
def file_type(url):
    """
    Returns the type of file based on extension:
    'image' | 'pdf' | 'file'
    """
    if not url:
        return 'file'
    url = url.lower()
    if url.endswith(('.jpg', '.jpeg', '.png', '.gif')):
        return 'image'
    elif url.endswith('.pdf'):
        return 'pdf'
    return 'file'