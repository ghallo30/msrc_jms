# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0002_issue_special_issue'),
        ('articles', '0015_article_current_rounds'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='issue',
        ),
        migrations.RemoveField(
            model_name='article',
            name='volume_number',
        ),
        migrations.AddField(
            model_name='article',
            name='article_issue',
            field=models.ForeignKey(null=True, to='issues.Issue'),
        ),
    ]
