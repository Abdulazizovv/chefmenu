from django import template


register = template.Library()

@register.filter(name="get_quantity")
def get_quantity(d, k):
    """Returns the quantity of the given key from a dictionary."""
    if str(k) in d:
        return d[str(k)]['quantity']
    return None