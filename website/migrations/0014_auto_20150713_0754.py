# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0013_auto_20150713_0752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='summary',
            name='bookmarks',
            field=models.ManyToManyField(related_name='summaries_bookmarked', blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
