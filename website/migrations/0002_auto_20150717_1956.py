# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import adminsortable.fields


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('order', models.PositiveIntegerField(editable=False, default=1, db_index=True)),
                ('name', models.CharField(max_length=100)),
                ('hebrew_name', models.CharField(max_length=100)),
                ('Subject', adminsortable.fields.SortableForeignKey(to='website.Subject')),
            ],
            options={
                'ordering': ['order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('order', models.PositiveIntegerField(editable=False, default=1, db_index=True)),
                ('name', models.CharField(max_length=100)),
                ('hebrew_name', models.CharField(max_length=100)),
                ('Categorie', adminsortable.fields.SortableForeignKey(to='website.Category')),
            ],
            options={
                'ordering': ['order'],
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='categorie',
            name='Subject',
        ),
        migrations.RemoveField(
            model_name='subcategorie',
            name='Categorie',
        ),
        migrations.AlterField(
            model_name='summary',
            name='Categorie',
            field=models.ForeignKey(to='website.Category'),
        ),
        migrations.AlterField(
            model_name='summary',
            name='Subcategorie',
            field=models.ForeignKey(to='website.Subcategory'),
        ),
        migrations.DeleteModel(
            name='Categorie',
        ),
        migrations.DeleteModel(
            name='Subcategorie',
        ),
    ]
