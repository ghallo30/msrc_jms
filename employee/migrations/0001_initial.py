# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.contrib.auth.models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(blank=True, verbose_name='last login', null=True)),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('username', models.CharField(unique=True, error_messages={'unique': 'A user with that username already exists.'}, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], verbose_name='username', help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=30)),
                ('first_name', models.CharField(blank=True, verbose_name='first name', max_length=30)),
                ('last_name', models.CharField(blank=True, verbose_name='last name', max_length=30)),
                ('email', models.EmailField(blank=True, verbose_name='email address', max_length=254)),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status', help_text='Designates whether the user can log into this admin site.')),
                ('is_active', models.BooleanField(default=True, verbose_name='active', help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_type', models.CharField(choices=[('AUTH', 'Author'), ('EDIT', 'Editor'), ('REV', 'Reviewer'), ('ADM', 'Admin'), ('COA', 'Co-Author')], max_length=5)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('contact_no', models.CharField(null=True, max_length=20)),
                ('address', models.CharField(null=True, max_length=120)),
                ('email_address', models.CharField(null=True, max_length=120)),
                ('affiliation', models.CharField(null=True, max_length=120)),
                ('department', models.CharField(null=True, max_length=120)),
                ('position_title', models.CharField(null=True, max_length=120)),
                ('degree', models.CharField(null=True, max_length=120)),
                ('research_interest', models.CharField(null=True, max_length=420)),
                ('fax_number', models.CharField(null=True, max_length=20)),
                ('groups', models.ManyToManyField(blank=True, related_query_name='user', related_name='user_set', verbose_name='groups', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', to='auth.Group')),
                ('user_permissions', models.ManyToManyField(blank=True, related_query_name='user', related_name='user_set', verbose_name='user permissions', help_text='Specific permissions for this user.', to='auth.Permission')),
            ],
            options={
                'verbose_name': 'user',
                'abstract': False,
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
