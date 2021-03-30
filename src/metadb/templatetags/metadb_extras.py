from django import template
from django.contrib.staticfiles import finders

register = template.Library()

@register.filter
def print_static(name):
    try:
        with open(finders.find(name), 'r') as f:
            return f.read()
    except IOError:
        return ''
    except TypeError:
        print(f'Warning! Form JS-file {name} is absent!')
        return ''
