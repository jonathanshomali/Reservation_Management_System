from django import template

register = template.Library()

@register.filter
def nights(check_out, check_in):
    delta = check_out - check_in
    return delta.days
