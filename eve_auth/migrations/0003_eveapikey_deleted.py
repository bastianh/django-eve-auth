# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eve_auth', '0002_auto_20150915_2017'),
    ]

    operations = [
        migrations.AddField(
            model_name='eveapikey',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
