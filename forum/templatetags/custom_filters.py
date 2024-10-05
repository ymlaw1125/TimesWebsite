from django import template
from django.utils import timezone
from datetime import timedelta

register = template.Library()

@register.filter
def time_since(value):
    now = timezone.now()
    diff = now - value

    if diff < timedelta(minutes=1):
        return f"{int(diff.seconds)} seconds ago"
    elif diff < timedelta(hours=1):
        return f"{int(diff.seconds // 60)} minutes ago"
    elif diff < timedelta(days=1):
        return f"{int(diff.seconds // 3600)} hours ago"
    elif diff < timedelta(weeks=1):
        return f"{int(diff.days)} days ago"
    elif diff < timedelta(weeks=4):
        return f"{int(diff.days // 7)} weeks ago"
    elif diff < timedelta(days=365):
        return value.strftime("%b %d")  # e.g., "Apr 12"
    else:
        return value.strftime("%b %d, %Y")  # e.g., "Apr 12, 2023"
