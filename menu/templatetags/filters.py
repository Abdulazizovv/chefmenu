from django import template

register = template.Library()


@register.filter
def get_category_count(category_counts, category):
    return category_counts.get(category, 0)    