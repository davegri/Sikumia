# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_auto_20150802_1944'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='karma',
        ),
    ]
