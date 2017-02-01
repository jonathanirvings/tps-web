# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-07 07:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0062_problemdata_statement'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testcase',
            name='subtasks',
        ),
        migrations.AddField(
            model_name='subtask',
            name='testcases',
            field=models.ManyToManyField(to='problems.TestCase', verbose_name='testcases'),
        ),
        migrations.AlterField(
            model_name='problemdata',
            name='statement',
            field=models.TextField(blank=True, default='', verbose_name='statement'),
        ),
    ]
