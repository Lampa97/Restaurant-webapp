from django import template

register = template.Library()


@register.filter()
def media_filter(path):
    if path:
        return f"/media/{path}"
    return "#"

@register.filter()
def dict_key(dictionary, key):
    """Retrieve a value from a dictionary by key."""
    return dictionary.get(key, [])
