# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-22 16:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0006_validatorresult'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problemrevision',
            name='parent_revision',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='problems.ProblemRevision', verbose_name='parent revision'),
        ),
        migrations.AlterField(
            model_name='testcase',
            name='_input_file',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='file_repository.FileModel'),
        ),
        migrations.AlterField(
            model_name='testcase',
            name='_output_file',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='file_repository.FileModel'),
        ),
    ]
