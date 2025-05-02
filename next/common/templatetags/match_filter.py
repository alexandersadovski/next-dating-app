from django import template

register = template.Library()


@register.filter
def other_user_pk(match, current_user):
    return match.user2.pk if match.user1 == current_user else match.user1.pk
