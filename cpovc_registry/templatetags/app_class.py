from django import template

register = template.Library()


@register.filter(name='get_class')
def get_class(value, args):
    # print('value', value, 'args', args)
    if value == args:
        return 'active'
    elif args in value:
        return 'active'
    else:
        split_vals = value.split('/')
        if split_vals[1] == args:
            return 'active'
        else:
            return ''
