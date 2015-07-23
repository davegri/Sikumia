# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import adminsortable.fields
from django.conf import settings
import django.utils.timezone
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('order', models.PositiveIntegerField(db_index=True, editable=False, default=1)),
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
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('content', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_edited', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subcategorie',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('order', models.PositiveIntegerField(db_index=True, editable=False, default=1)),
                ('name', models.CharField(max_length=100)),
                ('hebrew_name', models.CharField(max_length=100)),
                ('Categorie', adminsortable.fields.SortableForeignKey(to='website.Categorie')),
            ],
            options={
                'abstract': False,
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('order', models.PositiveIntegerField(db_index=True, editable=False, default=1)),
                ('name', models.CharField(max_length=100)),
                ('hebrew_name', models.CharField(max_length=100)),
                ('color', models.CharField(max_length=6)),
            ],
            options={
                'abstract': False,
                'ordering': ['order'],
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
                ('Categorie', models.ForeignKey(to='website.Categorie')),
                ('Subcategorie', models.ForeignKey(to='website.Subcategorie')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='summaries_authored')),
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
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('ip', models.CharField(max_length=40)),
                ('session', models.CharField(max_length=40)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('summary', models.ForeignKey(to='website.Summary', related_name='views')),
            ],
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
            model_name='categorie',
            name='Subject',
            field=adminsortable.fields.SortableForeignKey(to='website.Subject'),
        ),
    ]
