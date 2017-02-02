# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-02-02 21:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0065_auto_20170201_1911'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='script',
            name='problem',
        ),
        migrations.RemoveField(
            model_name='testcase',
            name='script',
        ),
        migrations.AddField(
            model_name='inputgenerator',
            name='is_enabled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='inputgenerator',
            name='text_data',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='testcase',
            name='generator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='problems.InputGenerator'),
        ),
        migrations.DeleteModel(
            name='Script',
        ),
    ]