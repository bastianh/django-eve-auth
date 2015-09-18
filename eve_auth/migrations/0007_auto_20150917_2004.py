# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eve_auth', '0006_eveapicall'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eveapicall',
            name='api_error_code',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='eveapicall',
            name='api_error_message',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='eveapicall',
            name='apikey',
            field=models.ForeignKey(null=True, to='eve_auth.EveApiKey'),
        ),
        migrations.AlterField(
            model_name='eveapicall',
            name='http_error_code',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='eveapicall',
            name='http_error_message',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='eveapicall',
            name='params',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='eveapicall',
            name='result_expires',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='eveapicall',
            name='result_timestamp',
            field=models.DateTimeField(null=True),
        ),
    ]
