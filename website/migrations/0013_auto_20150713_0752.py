# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0012_remove_summary__score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='summary',
            name='bookmarks',
            field=models.ManyToManyField(null=True, to=settings.AUTH_USER_MODEL, related_name='summaries_bookmarked'),
        ),
    ]
