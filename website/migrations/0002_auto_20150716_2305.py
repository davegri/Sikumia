# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subject',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='subject',
            name='order',
            field=models.PositiveIntegerField(db_index=True, default=1, editable=False),
        ),
        migrations.AlterField(
            model_name='subjectdivision',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, to='website.SubjectDivision'),
        ),
    ]
