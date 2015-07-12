# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_auto_20150712_0241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='summary',
            name='grade',
            field=models.IntegerField(choices=[(10, 'Grade 10'), (11, 'Grade 10'), (12, 'Grade 10')]),
        ),
    ]
