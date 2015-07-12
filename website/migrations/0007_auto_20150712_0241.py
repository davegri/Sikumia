# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_auto_20150712_0121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='summary',
            name='grade',
            field=models.IntegerField(choices=[('Grade 10', 'Grade 10'), ('Grade 11', 'Grade 11'), ('Grade 12', 'Grade 11')]),
        ),
    ]
