# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eve_auth', '0003_eveapikey_deleted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eveapikey',
            name='key_type',
            field=models.CharField(max_length=8, choices=[('char', 'Character'), ('corp', 'Corporation'), ('account', 'Account')]),
        ),
    ]
