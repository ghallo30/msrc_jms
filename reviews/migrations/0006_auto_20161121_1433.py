# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews', '0005_auto_20161111_1054'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewerForm',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('form_text', models.CharField(null=True, max_length=250)),
                ('form_value', models.CharField(null=True, max_length=250)),
                ('form_type', models.CharField(choices=[('T', 'text'), ('S', 'select'), ('C', 'check')], max_length=4, default='T')),
                ('form_name', models.CharField(null=True, max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('is_hidden', models.BooleanField(default=False)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='editordecision',
            name='decision',
            field=models.CharField(null=True, choices=[('ACC', 'Accepted Submission'), ('REV', 'Revision Required'), ('RES', 'Resubmit for Review'), ('DEC', 'Decline Submission')], max_length=4),
        ),
        migrations.AlterField(
            model_name='reviewdetails',
            name='familiarity',
            field=models.CharField(choices=[('H', 'High'), ('M', 'Moderate'), ('L', 'Low')], max_length=2, default='M'),
        ),
    ]
