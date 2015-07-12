# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('website', '0005_auto_20150711_2001'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='summary',
            name='negative_ratings',
        ),
        migrations.AddField(
            model_name='summary',
            name='negative_ratings',
            field=models.ManyToManyField(related_name='summary_negative_ratings', blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='summary',
            name='positive_ratings',
        ),
        migrations.AddField(
            model_name='summary',
            name='positive_ratings',
            field=models.ManyToManyField(related_name='summary_positive_ratings', blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
