# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields
import adminsortable.fields
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0007_auto_20150815_1454'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('order', models.PositiveIntegerField(db_index=True, default=1, editable=False)),
                ('name', models.CharField(max_length=100)),
                ('hebrew_name', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('content', models.TextField(max_length=1000)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_edited', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('order', models.PositiveIntegerField(db_index=True, default=1, editable=False)),
                ('name', models.CharField(max_length=100)),
                ('hebrew_name', models.CharField(max_length=100)),
                ('category', adminsortable.fields.SortableForeignKey(to='website.Category')),
            ],
            options={
                'ordering': ['order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('order', models.PositiveIntegerField(db_index=True, default=1, editable=False)),
                ('name', models.CharField(max_length=100)),
                ('hebrew_name', models.CharField(max_length=100)),
                ('color', models.CharField(max_length=6)),
                ('categories_per_line', models.IntegerField(default=4)),
            ],
            options={
                'ordering': ['order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Summary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=128)),
                ('content', ckeditor.fields.RichTextField()),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_edited', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, related_name='profile')),
            ],
        ),
        migrations.CreateModel(
            name='View',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('ip', models.CharField(max_length=40)),
                ('session', models.CharField(max_length=40)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('summary', models.ForeignKey(related_name='views', to='website.Summary')),
            ],
        ),
        migrations.AddField(
            model_name='summary',
            name='author',
            field=models.ForeignKey(related_name='summaries_authored', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='summary',
            name='category',
            field=models.ForeignKey(to='website.Category'),
        ),
        migrations.AddField(
            model_name='summary',
            name='subcategory',
            field=models.ForeignKey(to='website.Subcategory'),
        ),
        migrations.AddField(
            model_name='summary',
            name='subject',
            field=models.ForeignKey(to='website.Subject'),
        ),
        migrations.AddField(
            model_name='summary',
            name='users_bookmarked',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True, related_name='summaries_bookmarked'),
        ),
        migrations.AddField(
            model_name='summary',
            name='users_rated_negative',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True, related_name='summaries_rated_negative'),
        ),
        migrations.AddField(
            model_name='summary',
            name='users_rated_positive',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True, related_name='summaries_rated_positive'),
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
            field=adminsortable.fields.SortableForeignKey(related_name='categories', to='website.Subject'),
        ),
    ]
