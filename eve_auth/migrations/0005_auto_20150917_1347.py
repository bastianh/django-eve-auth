# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('eve_auth', '0004_auto_20150916_1847'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eveapikey',
            name='modified',
        ),
        migrations.AddField(
            model_name='eveapikey',
            name='updated',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='eveapikey',
            name='created',
            field=model_utils.fields.AutoCreatedField(editable=False, default=django.utils.timezone.now),
        ),
    ]
