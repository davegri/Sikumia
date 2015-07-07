# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import ckeditor.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Summary',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('subject', models.CharField(max_length=20, choices=[('english', 'english'), ('bible', 'bible'), ('history', 'history'), ('civics', 'civics'), ('language', 'language'), ('literature', 'literature')])),
                ('content', ckeditor.fields.RichTextField(null=True, blank=True)),
                ('date_created', models.DateTimeField(default=datetime.datetime(2015, 7, 7, 19, 45, 37, 911189))),
                ('date_edited', models.DateTimeField(null=True, blank=True)),
                ('views', models.IntegerField(default=0)),
                ('author', models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
    ]
