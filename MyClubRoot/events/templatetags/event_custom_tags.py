from django import template
from django.template.defaultfilters import stringfilter
from datetime import datetime

register = template.Library()

@register.inclusion_tag('events/announcements.html')
def announcements():
    announcements = [
        {
            'date': '6-10-2020',
            'announcement': 'club registration'
        }
    ]
    return {'announcements': announcements}

@register.simple_tag
def create_date(date_val):
    return 'This content was created on %s' % date_val.strftime('%A %B %d, %Y')

@register.filter(name='reverse')
@stringfilter
def reverse(value):
    return value[::-1]