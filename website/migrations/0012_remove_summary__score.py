# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0011_auto_20150713_0702'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='summary',
            name='_score',
        ),
    ]
