# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import adminsortable.fields


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20150728_0352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='subject',
            field=adminsortable.fields.SortableForeignKey(to='website.Subject', related_name='categories'),
        ),
    ]
