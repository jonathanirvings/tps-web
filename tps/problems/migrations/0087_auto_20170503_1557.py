# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-05-03 15:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0086_merge'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='solutionsubtaskexpectedscore',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='solutionsubtaskexpectedscore',
            name='solution',
        ),
        migrations.RemoveField(
            model_name='solutionsubtaskexpectedscore',
            name='subtask',
        ),
        migrations.AlterUniqueTogether(
            name='solutiontestexpectedscore',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='solutiontestexpectedscore',
            name='solution',
        ),
        migrations.RemoveField(
            model_name='solutiontestexpectedscore',
            name='testcase',
        ),
        migrations.AlterModelOptions(
            name='solution',
            options={'ordering': ('problem', 'name')},
        ),
        migrations.DeleteModel(
            name='SolutionSubtaskExpectedScore',
        ),
        migrations.DeleteModel(
            name='SolutionTestExpectedScore',
        ),
    ]
