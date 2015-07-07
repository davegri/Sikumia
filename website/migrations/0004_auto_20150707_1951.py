# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_auto_20150707_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='summary',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
