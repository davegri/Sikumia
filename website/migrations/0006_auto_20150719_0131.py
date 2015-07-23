# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_auto_20150718_1811'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='Subject',
            new_name='subject',
        ),
        migrations.RenameField(
            model_name='subcategory',
            old_name='Category',
            new_name='category',
        ),
    ]
