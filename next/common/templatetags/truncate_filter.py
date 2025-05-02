from django import template

register = template.Library()


@register.filter
def truncate(value, length: int):
    if len(value) > length:
        return value[:length] + '...'
    return value
