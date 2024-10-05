from django import template

register = template.Library()

@register.filter
def filter(things, category):
    return things.filter(user=category).first()