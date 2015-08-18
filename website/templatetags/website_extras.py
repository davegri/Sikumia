from django import template
from django.template.defaultfilters import stringfilter
import django.utils.timezone

import datetime

from django import template

register = template.Library()

@register.filter
@stringfilter
def toHebrew(subject):
    """converts name of subject in english to hebrew"""
    subjectDict = {
        'english': 'אנגלית',
        'bible': 'תנ"ך',
        'history': 'היסטוריה',
        'civics': 'אזרחות',
        'language': 'לשון',
        'literature': 'ספרות',
    }
    return subjectDict[subject]



register = template.Library()


@register.filter(name='timesince_human')
def humanize_timesince(date):
    delta = django.utils.timezone.now() - date

    num_years = delta.days / 365
    if (int(num_years) > 0):
        return "לפני %d שנים" %num_years
    num_weeks = delta.days / 7
    if (int(num_weeks) > 0):
        return "לפני %d שבועות" %num_weeks
    if (delta.days > 0):
        return "לפני %d ימים" %delta.days
    num_hours = delta.seconds / 3600
    if (int(num_hours) > 0):
        return "לפני %d שעות" %num_hours
    num_minutes = delta.seconds / 60
    if (int(num_minutes) > 0):
        return "לפני %d דקות" %num_minutes
    return "לפני כמה שניות"