# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_auto_20150707_1951'),
    ]

    operations = [
        migrations.AddField(
            model_name='summary',
            name='grade',
            field=models.IntegerField(default=10, choices=[('Grade 10', '10'), ('Grade 11', '11'), ('Grade 12', '12')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='summary',
            name='negative_ratings',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='summary',
            name='positive_ratings',
            field=models.IntegerField(default=0),
        ),
    ]
