from django import template
from django.utils.timezone import now

register = template.Library()


@register.filter
def timestamp_format(value):
    today = now().date()
    delta = today - value.date()

    if delta.days == 0:
        return value.strftime("%I:%M %p")
    elif delta.days < 7:
        return value.strftime("%a")
    else:
        return value.strftime("%d/%m/%Y")
