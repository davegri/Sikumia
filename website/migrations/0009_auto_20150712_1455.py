# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_auto_20150712_0242'),
    ]

    operations = [
        migrations.CreateModel(
            name='SummaryView',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=40)),
                ('session', models.CharField(max_length=40)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.RemoveField(
            model_name='summary',
            name='views',
        ),
        migrations.AlterField(
            model_name='summary',
            name='grade',
            field=models.IntegerField(choices=[(10, 'Grade 10'), (11, 'Grade 11'), (12, 'Grade 12')]),
        ),
        migrations.AddField(
            model_name='summaryview',
            name='summary',
            field=models.ForeignKey(to='website.Summary', related_name='views'),
        ),
    ]
