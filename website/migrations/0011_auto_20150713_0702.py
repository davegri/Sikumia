# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('website', '0010_auto_20150713_0626'),
    ]

    operations = [
        migrations.AddField(
            model_name='summary',
            name='_score',
            field=models.DecimalField(decimal_places=15, default=0.0, max_digits=18),
        ),
        migrations.AlterField(
            model_name='summary',
            name='author',
            field=models.ForeignKey(related_name='summaries_authored', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='summary',
            name='bookmarks',
        ),
        migrations.AddField(
            model_name='summary',
            name='bookmarks',
            field=models.ManyToManyField(related_name='summaries_bookmarked', to=settings.AUTH_USER_MODEL),
        ),
    ]
