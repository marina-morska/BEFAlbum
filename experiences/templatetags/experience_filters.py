from django import template

register = template.Library()

@register.filter
def shorten_text(value):
    if len(value) > 50:
        return value[:50].rsplit(' ', 1)[0] + '...'
    return value

