# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields
import django.utils.timezone
import adminsortable.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0007_auto_20150812_0010'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True, default=1)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('content', models.TextField(max_length=1000)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_edited', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True, default=1)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True, default=1)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('content', ckeditor.fields.RichTextField(default='ברירת מחדל')),
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
                ('user', models.OneToOneField(related_name='profile', serialize=False, primary_key=True, to=settings.AUTH_USER_MODEL)),
                ('rank', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='View',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('ip', models.CharField(max_length=40)),
                ('session', models.CharField(max_length=40)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('summary', models.ForeignKey(to='website.Summary', related_name='views')),
            ],
        ),
        migrations.AddField(
            model_name='summary',
            name='author',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='summaries_authored'),
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
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, related_name='summaries_bookmarked'),
        ),
        migrations.AddField(
            model_name='summary',
            name='users_rated_negative',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, related_name='summaries_rated_negative'),
        ),
        migrations.AddField(
            model_name='summary',
            name='users_rated_positive',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, related_name='summaries_rated_positive'),
        ),
        migrations.AddField(
            model_name='comment',
            name='summary',
            field=models.ForeignKey(to='website.Summary', related_name='comments'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='comments'),
        ),
        migrations.AddField(
            model_name='category',
            name='subject',
            field=adminsortable.fields.SortableForeignKey(to='website.Subject', related_name='categories'),
        ),
    ]
