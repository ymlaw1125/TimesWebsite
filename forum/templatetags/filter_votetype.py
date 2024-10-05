from django import template

register = template.Library()

@register.filter
def votetype(things, category):
    if things.filter(user=category).first(): return things.filter(user=category).first().vote_type