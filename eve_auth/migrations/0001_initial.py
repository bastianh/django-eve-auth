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
            name='EveApiKey',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(verbose_name='created', editable=False, default=django.utils.timezone.now)),
                ('modified', model_utils.fields.AutoLastModifiedField(verbose_name='modified', editable=False, default=django.utils.timezone.now)),
                ('key_id', models.IntegerField()),
                ('vcode', models.CharField(max_length=255)),
                ('status', model_utils.fields.StatusField(choices=[('new', 'new'), ('active', 'active'), ('error', 'error'), ('deleted', 'deleted')], max_length=100, no_check_for_status=True, default='new')),
                ('access_mask', models.IntegerField(null=True)),
                ('key_type', models.CharField(choices=[('char', 'Character'), ('corp', 'Corporation')], max_length=2)),
                ('expires', models.DateTimeField()),
                ('status_changed', model_utils.fields.MonitorField(monitor='status', default=django.utils.timezone.now)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EveCharacter',
            fields=[
                ('character_id', models.IntegerField(serialize=False, primary_key=True)),
                ('character_name', models.CharField(max_length=200)),
                ('updated', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EveCorporation',
            fields=[
                ('corporation_id', models.IntegerField(serialize=False, primary_key=True)),
                ('corporation_name', models.CharField(max_length=200)),
                ('alliance_id', models.IntegerField(null=True)),
                ('alliance_name', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EveLoginToken',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('scopes', models.CharField(max_length=200)),
                ('token_type', models.CharField(max_length=200)),
                ('character_owner_hash', models.CharField(max_length=200)),
                ('character', models.ForeignKey(to='eve_auth.EveCharacter')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='evecharacter',
            name='corporation',
            field=models.ForeignKey(to='eve_auth.EveCorporation', null=True),
        ),
        migrations.AddField(
            model_name='eveapikey',
            name='characters',
            field=models.ManyToManyField(to='eve_auth.EveCharacter'),
        ),
        migrations.AddField(
            model_name='eveapikey',
            name='corporation',
            field=models.ForeignKey(to='eve_auth.EveCorporation', null=True),
        ),
        migrations.AddField(
            model_name='eveapikey',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='evelogintoken',
            unique_together=set([('character', 'character_owner_hash')]),
        ),
    ]
