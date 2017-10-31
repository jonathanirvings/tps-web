# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-11 18:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('runner', '0004_jobmodel_compile_job_squashed_0007_jobmodel_isolate_log'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='jobfile',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='jobfile',
            name='file_model',
        ),
        migrations.RemoveField(
            model_name='jobfile',
            name='job_model',
        ),
        migrations.RemoveField(
            model_name='jobmodel',
            name='files',
        ),
        migrations.DeleteModel(
            name='JobFile',
        ),
        migrations.DeleteModel(
            name='JobModel',
        ),
    ]