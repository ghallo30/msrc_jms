# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0002_remove_user_email_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='receive_new_announcement',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='user',
            name='receive_new_issue',
            field=models.BooleanField(default=True),
        ),
    ]
