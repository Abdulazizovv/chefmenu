from django import template

register = template.Library()


@register.filter(name="dict_key")
def dict_key(d, k):
    """Returns the given key from a dictionary."""
    print(d, k)
    if str(k) in d:
        return d[str(k)]
    return None



