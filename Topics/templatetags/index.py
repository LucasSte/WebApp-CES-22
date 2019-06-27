from django import template
register = template.Library()


@register.filter
def remove_first(List):
    first = List[0]
    List[:] = List[1:]
    return first
