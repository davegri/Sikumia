# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('website', '0009_auto_20150712_1455'),
    ]

    operations = [
        migrations.AddField(
            model_name='summary',
            name='bookmarks',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, related_name='bookmarked'),
        ),
        migrations.AlterField(
            model_name='summary',
            name='author',
            field=models.ForeignKey(related_name='authored', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='summary',
            name='negative_ratings',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, related_name='summaries_rated_negative'),
        ),
        migrations.AlterField(
            model_name='summary',
            name='positive_ratings',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, related_name='summaries_rated_positive'),
        ),
    ]
