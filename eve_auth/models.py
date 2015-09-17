from django.db import models
from django.conf import settings
from model_utils import Choices
from model_utils.fields import StatusField, MonitorField
from model_utils.models import TimeStampedModel


class EveCorporation(models.Model):
    corporation_id = models.IntegerField(primary_key=True)
    corporation_name = models.CharField(max_length=200)
    alliance_id = models.IntegerField(null=True)
    alliance_name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.corporation_name


class EveCharacter(models.Model):
    character_id = models.IntegerField(primary_key=True)
    character_name = models.CharField(max_length=200)
    corporation = models.ForeignKey(EveCorporation, null=True)
    updated = models.DateTimeField(null=True)

    def __str__(self):
        return self.character_name


class EveApiKey(TimeStampedModel):
    STATUS = Choices('unverified', 'active', 'error', 'suspended')
    KEY_TYPES = (('char', 'Character'), ('corp', 'Corporation'), ('account', 'Account'))

    key_id = models.IntegerField()
    vcode = models.CharField(max_length=255)

    status = StatusField(default='unverified')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    characters = models.ManyToManyField(EveCharacter)
    corporation = models.ForeignKey(EveCorporation, null=True)
    access_mask = models.IntegerField(null=True)
    key_type = models.CharField(choices=KEY_TYPES, max_length=8)
    expires = models.DateTimeField(null=True)
    deleted = models.BooleanField(default=False)

    status_changed = MonitorField(monitor='status')


class EveLoginToken(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    character = models.ForeignKey(EveCharacter)
    scopes = models.CharField(max_length=200)
    token_type = models.CharField(max_length=200)
    character_owner_hash = models.CharField(max_length=200)

    def __str__(self):
        return "token {}".format(self.character_id)

    class Meta:
        unique_together = ('character', 'character_owner_hash')
