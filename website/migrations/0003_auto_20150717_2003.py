# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20150717_1956'),
    ]

    operations = [
        migrations.RenameField(
            model_name='summary',
            old_name='Categorie',
            new_name='Category',
        ),
        migrations.RenameField(
            model_name='summary',
            old_name='Subcategorie',
            new_name='Subcategory',
        ),
    ]
