# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_auto_20150717_2003'),
    ]

    operations = [
        migrations.RenameField(
            model_name='summary',
            old_name='Category',
            new_name='category',
        ),
        migrations.RenameField(
            model_name='summary',
            old_name='Subcategory',
            new_name='subcategory',
        ),
    ]
