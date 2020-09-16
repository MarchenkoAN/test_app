
from django import template
from django.utils.dateparse import parse_datetime
from django.utils.html import mark_safe

from django.utils.datetime_safe import date, datetime

register = template.Library()

@register.filter(name='dateWithZeroBasedMonth')
def dateWithZeroBasedMonth(value):
    if value is None:
        value = datetime.now()
    year = value.year
    month = value.month
    day = value.day
    hours = value.hour
    minutes = value.minute
    seconds = value.second
    return str(year) + "," + str(month-1) + "," + str(day) + "," + str(hours) + "," + str(minutes) + "," + str(seconds)