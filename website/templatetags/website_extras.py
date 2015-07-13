from django import template
from django.template.defaultfilters import stringfilter

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
