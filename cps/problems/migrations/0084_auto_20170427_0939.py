# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-04-27 09:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0083_auto_20170427_0928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solutionsubtaskexpectedverdict',
            name='solution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subtask_verdicts', to='problems.Solution', verbose_name='solution'),
        ),
        migrations.AlterField(
            model_name='testcase',
            name='judge_initialization_successful',
            field=models.NullBooleanField(default=False, verbose_name='initialization finished'),
        ),
    ]
