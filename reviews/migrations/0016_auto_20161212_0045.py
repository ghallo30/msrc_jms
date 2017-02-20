# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0015_reviewdetails_acceptability'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewFormItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('required', models.BooleanField(default=True)),
                ('included', models.BooleanField(default=True)),
                ('review_form', models.ForeignKey(to='reviews.ReviewForm', null=True)),
                ('review_item', models.ForeignKey(to='reviews.ReviewerElement', null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='reviewerresponse',
            name='review_form',
        ),
        migrations.AddField(
            model_name='reviewerresponse',
            name='review_details',
            field=models.ForeignKey(to='reviews.ReviewDetails', null=True),
        ),
    ]
