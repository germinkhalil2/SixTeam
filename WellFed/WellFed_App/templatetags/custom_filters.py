from django import template

register = template.Library()

@register.filter
def div(value, arg):
    try:
        return (float(value) / float(arg)) * 100 if arg else 0
    except (ValueError, ZeroDivisionError):
        return 0
