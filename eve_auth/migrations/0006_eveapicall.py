# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('eve_auth', '0005_auto_20150917_1347'),
    ]

    operations = [
        migrations.CreateModel(
            name='EveApiCall',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('path', models.CharField(max_length=150)),
                ('params', models.TextField()),
                ('success', models.BooleanField(default=False)),
                ('created', model_utils.fields.AutoCreatedField(editable=False, default=django.utils.timezone.now)),
                ('result_timestamp', models.DateTimeField()),
                ('result_expires', models.DateTimeField()),
                ('api_error_code', models.IntegerField()),
                ('api_error_message', models.CharField(max_length=255)),
                ('http_error_code', models.IntegerField()),
                ('http_error_message', models.CharField(max_length=255)),
                ('apikey', models.ForeignKey(to='eve_auth.EveApiKey')),
            ],
        ),
    ]
