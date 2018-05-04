from django import template

register = template.Library()


@register.filter(name='enumerate')
def enumerate_list(value: [str]):
    if value:
        return enumerate(value, start=1)
