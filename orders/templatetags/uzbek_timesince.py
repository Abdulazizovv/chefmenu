from django import template
from django.utils.timesince import timesince as timesince_
from django.utils.timezone import now as now_

register = template.Library()

@register.filter
def uzbek_timesince(value):
    periods = (
        (60, 'soniya', 'soniya'),
        (3600, 'daqiqa', 'daqiqa'),
        (86400, 'soat', 'soat'),
        (604800, 'kun', 'kun'),
        (2419200, 'hafta', 'hafta'),
        (29030400, 'oy', 'oy'),
    )

    def format(difference, period):
        return "%(time)s %(period)s avval" % {'time': difference, 'period': period}

    difference = now_() - value

    for period_seconds, singular, plural in periods:
        if difference.seconds < period_seconds:
            return format(difference.seconds // (period_seconds // 60), singular if difference.seconds < 120 else plural)
    return 'hozirgina'


