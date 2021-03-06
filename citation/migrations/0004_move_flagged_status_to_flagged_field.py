# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-15 19:03
from __future__ import unicode_literals

from django.db import migrations, models


def forwards_func(apps, schema_editor):
    Publication = apps.get_model('citation', 'Publication')
    db_alias = schema_editor.connection.alias
    Publication.objects.using(db_alias).filter(status='FLAGGED').update(status='UNTAGGED', flagged=True)


def reverse_func(apps, schema_editor):
    Publication = apps.get_model('citation', 'Publication')
    db_alias = schema_editor.connection.alias
    Publication.objects.using(db_alias).filter(flagged=True).update(status='FLAGGED', flagged=False)


class Migration(migrations.Migration):
    dependencies = [
        ('citation', '0003_auto_20160915_1915'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func)
    ]
