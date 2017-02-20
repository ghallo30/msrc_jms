# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0020_auto_20170110_0225'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='subtitle',
            new_name='art_number',
        ),
    ]
