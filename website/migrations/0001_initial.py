# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import adminsortable.fields
import ckeditor.fields
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('order', models.PositiveIntegerField(default=1, db_index=True, editable=False)),
                ('name', models.CharField(max_length=100)),
                ('hebrew_name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('content', models.TextField(max_length=1000)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_edited', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('order', models.PositiveIntegerField(default=1, db_index=True, editable=False)),
                ('name', models.CharField(max_length=100)),
                ('hebrew_name', models.CharField(max_length=100)),
                ('category', adminsortable.fields.SortableForeignKey(to='website.Category')),
            ],
            options={
                'abstract': False,
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('order', models.PositiveIntegerField(default=1, db_index=True, editable=False)),
                ('name', models.CharField(max_length=100)),
                ('hebrew_name', models.CharField(max_length=100)),
                ('color', models.CharField(max_length=6)),
                ('categories_per_line', models.IntegerField(default=4)),
            ],
            options={
                'abstract': False,
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Summary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=128)),
                ('content', ckeditor.fields.RichTextField(null=True, blank=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_edited', models.DateTimeField(null=True, blank=True)),
                ('author', models.ForeignKey(related_name='summaries_authored', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(to='website.Category')),
                ('subcategory', models.ForeignKey(to='website.Subcategory')),
                ('subject', models.ForeignKey(to='website.Subject')),
                ('users_bookmarked', models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True, related_name='summaries_bookmarked')),
                ('users_rated_negative', models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True, related_name='summaries_rated_negative')),
                ('users_rated_positive', models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True, related_name='summaries_rated_positive')),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='View',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('ip', models.CharField(max_length=40)),
                ('session', models.CharField(max_length=40)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('summary', models.ForeignKey(related_name='views', to='website.Summary')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='summary',
            field=models.ForeignKey(related_name='comments', to='website.Summary'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(related_name='comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='category',
            name='subject',
            field=adminsortable.fields.SortableForeignKey(to='website.Subject'),
        ),
    ]
