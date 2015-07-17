# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import adminsortable.fields
from django.conf import settings
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('content', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_edited', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('hebrew_name', models.CharField(max_length=100)),
                ('color', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='SubjectDivision',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('order', models.PositiveIntegerField(db_index=True, default=1, editable=False)),
                ('name', models.CharField(max_length=100)),
                ('hebrew_name', models.CharField(max_length=100)),
                ('Subject', adminsortable.fields.SortableForeignKey(related_name='divisions', to='website.Subject')),
                ('parent', adminsortable.fields.SortableForeignKey(null=True, blank=True, to='website.SubjectDivision')),
            ],
            options={
                'ordering': ['order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Summary',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=128)),
                ('content', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_edited', models.DateTimeField(blank=True, null=True)),
                ('author', models.ForeignKey(related_name='summaries_authored', to=settings.AUTH_USER_MODEL)),
                ('subject', models.ForeignKey(to='website.Subject')),
                ('subject_division', models.ForeignKey(null=True, to='website.SubjectDivision')),
                ('users_bookmarked', models.ManyToManyField(blank=True, related_name='summaries_bookmarked', to=settings.AUTH_USER_MODEL)),
                ('users_rated_negative', models.ManyToManyField(blank=True, related_name='summaries_rated_negative', to=settings.AUTH_USER_MODEL)),
                ('users_rated_positive', models.ManyToManyField(blank=True, related_name='summaries_rated_positive', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='SummaryView',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
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
    ]
