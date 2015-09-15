# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('eve_auth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eveapikey',
            name='expires',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='eveapikey',
            name='status',
            field=model_utils.fields.StatusField(default='unverified', choices=[(0, 'dummy')], max_length=100, no_check_for_status=True),
        ),
    ]
