from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def personal_number(value):
    return f"{value[:8]}-{value[8:]}"
