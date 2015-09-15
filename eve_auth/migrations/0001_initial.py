# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EveCharacter',
            fields=[
                ('character_id', models.IntegerField(primary_key=True, serialize=False)),
                ('character_name', models.CharField(max_length=200)),
                ('updated', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EveCorporation',
            fields=[
                ('corporation_id', models.IntegerField(primary_key=True, serialize=False)),
                ('corporation_name', models.CharField(max_length=200)),
                ('alliance_id', models.IntegerField(null=True)),
                ('alliance_name', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EveLoginToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
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
            field=models.ForeignKey(null=True, to='eve_auth.EveCorporation'),
        ),
        migrations.AlterUniqueTogether(
            name='evelogintoken',
            unique_together=set([('character', 'character_owner_hash')]),
        ),
    ]
