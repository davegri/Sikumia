# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import adminsortable.fields


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='subject',
            field=adminsortable.fields.SortableForeignKey(related_name='category', to='website.Subject'),
        ),
    ]
