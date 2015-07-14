# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0015_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='summary',
            name='bookmarks',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True, related_name='summaries_bookmarked'),
        ),
        migrations.AlterField(
            model_name='summary',
            name='grade',
            field=models.IntegerField(choices=[(10, "כיתה י'"), (11, "כיתה יא'"), (12, "כיתה יב'")]),
        ),
        migrations.AlterField(
            model_name='summary',
            name='subject',
            field=models.CharField(max_length=20, choices=[('english', 'אנגלית'), ('bible', 'תנ"ך'), ('history', 'היסטוריה'), ('civics', 'אזרחות'), ('language', 'לשון'), ('literature', 'ספרות')]),
        ),
    ]
