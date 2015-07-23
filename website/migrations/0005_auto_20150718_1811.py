# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_auto_20150717_2005'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subcategory',
            old_name='Categorie',
            new_name='Category',
        ),
    ]
