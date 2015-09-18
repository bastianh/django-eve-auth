from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from model_utils import Choices
from model_utils.fields import StatusField, MonitorField, AutoCreatedField
from model_utils.models import TimeStampedModel

from eve_auth.tasks import update_character_info


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


@receiver(post_save, sender=EveCharacter)
def character_handler(sender, instance, created, **kwargs):
    if created:
        update_character_info.apply_async([instance.character_id])


class EveApiKey(models.Model):
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
    updated = models.DateTimeField(null=True)
    status_changed = MonitorField(monitor='status')
    created = AutoCreatedField()

    def __str__(self):
        return "ApiKey %d" % self.key_id


class EveApiCall(models.Model):
    path = models.CharField(max_length=150)
    params = models.TextField(null=True)
    success = models.BooleanField(default=False)
    created = AutoCreatedField()

    result_timestamp = models.DateTimeField(null=True)
    result_expires = models.DateTimeField(null=True)

    apikey = models.ForeignKey(EveApiKey, null=True)

    api_error_code = models.IntegerField(null=True)
    api_error_message = models.CharField(null=True, max_length=255)
    http_error_code = models.IntegerField(null=True)
    http_error_message = models.CharField(null=True, max_length=255)


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
