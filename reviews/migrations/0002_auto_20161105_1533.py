# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_auto_20161105_1227'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EditorDecision',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('decision', models.CharField(max_length=500, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_decided', models.DateTimeField(null=True, verbose_name='date decided')),
                ('stage', models.CharField(max_length=500, null=True)),
                ('article', models.ForeignKey(null=True, to='articles.Article')),
                ('editor', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'editor_decision',
            },
        ),
        migrations.AddField(
            model_name='reviewdetails',
            name='assigned_by',
            field=models.ForeignKey(related_name='editor_assign', null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reviewdetails',
            name='date_confirmed',
            field=models.DateTimeField(null=True, verbose_name='date review confirmed'),
        ),
        migrations.AddField(
            model_name='reviewdetails',
            name='date_notified',
            field=models.DateTimeField(null=True, verbose_name='date notified'),
        ),
        migrations.AddField(
            model_name='reviewdetails',
            name='familiarity',
            field=models.CharField(max_length=2, default='M', choices=[('H', 'High'), ('L', 'Low'), ('M', 'Moderate')]),
        ),
        migrations.AddField(
            model_name='reviewdetails',
            name='invitation_accepted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='reviewdetails',
            name='invitation_declined',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='reviewdetails',
            name='replaced',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='reviewdetails',
            name='date_ended',
            field=models.DateTimeField(null=True, verbose_name='date ended'),
        ),
        migrations.AlterField(
            model_name='reviewdetails',
            name='date_start',
            field=models.DateTimeField(null=True, verbose_name='date started'),
        ),
        migrations.AlterField(
            model_name='reviewdetails',
            name='date_submitted',
            field=models.DateTimeField(null=True, verbose_name='date_review_submit'),
        ),
        migrations.AlterField(
            model_name='reviewdetails',
            name='reviewer',
            field=models.ForeignKey(related_name='reviewer', null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
