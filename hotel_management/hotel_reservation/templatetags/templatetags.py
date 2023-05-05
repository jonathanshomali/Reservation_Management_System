from django import template

register = template.Library()

@register.filter
def nights(check_out, check_in):
    return (check_out - check_in).days
