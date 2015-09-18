# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Alliance',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ApiCall',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('path', models.CharField(max_length=150)),
                ('params', models.TextField(null=True)),
                ('success', models.BooleanField(default=False)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False)),
                ('result_timestamp', models.DateTimeField(null=True)),
                ('result_expires', models.DateTimeField(null=True)),
                ('api_error_code', models.IntegerField(null=True)),
                ('api_error_message', models.CharField(max_length=255, null=True)),
                ('http_error_code', models.IntegerField(null=True)),
                ('http_error_message', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ApiKey',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('key_id', models.IntegerField()),
                ('vcode', models.CharField(max_length=255)),
                ('status', model_utils.fields.StatusField(default='unverified', choices=[('unverified', 'unverified'), ('active', 'active'), ('error', 'error'), ('suspended', 'suspended')], no_check_for_status=True, max_length=100)),
                ('access_mask', models.IntegerField(null=True)),
                ('key_type', models.CharField(choices=[('char', 'Character'), ('corp', 'Corporation'), ('account', 'Account')], max_length=8)),
                ('expires', models.DateTimeField(null=True)),
                ('deleted', models.BooleanField(default=False)),
                ('updated', models.DateTimeField(null=True)),
                ('status_changed', model_utils.fields.MonitorField(default=django.utils.timezone.now, monitor='status')),
                ('error_count', models.IntegerField(default=0)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('updated', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Corporation',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('alliance', models.ForeignKey(to='eve_auth.Alliance', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EveLoginToken',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('scopes', models.CharField(max_length=200)),
                ('token_type', models.CharField(max_length=200)),
                ('character_owner_hash', models.CharField(max_length=200)),
                ('character', models.ForeignKey(to='eve_auth.Character')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='character',
            name='corporation',
            field=models.ForeignKey(to='eve_auth.Corporation', null=True),
        ),
        migrations.AddField(
            model_name='apikey',
            name='characters',
            field=models.ManyToManyField(to='eve_auth.Character'),
        ),
        migrations.AddField(
            model_name='apikey',
            name='corporation',
            field=models.ForeignKey(to='eve_auth.Corporation', null=True),
        ),
        migrations.AddField(
            model_name='apikey',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='apicall',
            name='apikey',
            field=models.ForeignKey(to='eve_auth.ApiKey', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='evelogintoken',
            unique_together=set([('character', 'character_owner_hash')]),
        ),
    ]
