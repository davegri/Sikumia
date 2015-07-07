# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20150707_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='summary',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 7, 19, 49, 42, 284257, tzinfo=utc)),
        ),
    ]
