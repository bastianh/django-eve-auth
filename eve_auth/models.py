from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from model_utils import Choices
from model_utils.fields import StatusField, MonitorField, AutoCreatedField
from model_utils.models import TimeStampedModel

from eve_auth.tasks import update_character_info


class Alliance(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    @classmethod
    def get_or_create(cls, alliance_id, alliance_name) -> 'Alliance':
        object, _ = cls.objects.get_or_create(id=alliance_id, name=alliance_name)
        return object

    def __str__(self):
        return self.name


class Corporation(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    alliance = models.ForeignKey(Alliance, null=True)

    @classmethod
    def get_or_create(cls, corporation_id, corporation_name) -> 'Corporation':
        object, _ = cls.objects.get_or_create(id=corporation_id, name=corporation_name)
        return object

    def __str__(self):
        return self.name


class Character(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    corporation = models.ForeignKey(Corporation, null=True)
    updated = models.DateTimeField(null=True)

    @classmethod
    def get_or_create(cls, character_id, character_name) -> 'Character':
        object, _ = cls.objects.get_or_create(id=character_id, name=character_name)
        return object

    def __str__(self):
        return self.name


@receiver(post_save, sender=Character)
def character_handler(sender, instance, created, **kwargs):
    if created:
        update_character_info.apply_async([instance.id])


class ApiKey(models.Model):
    STATUS = Choices('unverified', 'active', 'error', 'suspended')
    KEY_TYPES = (('char', 'Character'), ('corp', 'Corporation'), ('account', 'Account'))

    key_id = models.IntegerField()
    vcode = models.CharField(max_length=255)

    status = StatusField(default='unverified')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    characters = models.ManyToManyField(Character)
    corporation = models.ForeignKey(Corporation, null=True)
    access_mask = models.IntegerField(null=True)
    key_type = models.CharField(choices=KEY_TYPES, max_length=8)
    expires = models.DateTimeField(null=True)

    deleted = models.BooleanField(default=False)
    updated = models.DateTimeField(null=True)
    status_changed = MonitorField(monitor='status')
    error_count = models.IntegerField(default=0)

    created = AutoCreatedField()

    def __str__(self):
        return "%d" % self.key_id


class ApiCall(models.Model):
    path = models.CharField(max_length=150)
    params = models.TextField(null=True)
    success = models.BooleanField(default=False)
    created = AutoCreatedField()

    result_timestamp = models.DateTimeField(null=True)
    result_expires = models.DateTimeField(null=True)

    apikey = models.ForeignKey(ApiKey, null=True)

    api_error_code = models.IntegerField(null=True)
    api_error_message = models.CharField(null=True, max_length=255)
    http_error_code = models.IntegerField(null=True)
    http_error_message = models.CharField(null=True, max_length=255)


class EveLoginToken(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    character = models.ForeignKey(Character)
    scopes = models.CharField(max_length=200)
    token_type = models.CharField(max_length=200)
    character_owner_hash = models.CharField(max_length=200)

    def __str__(self):
        return "token {}".format(self.character_id)

    class Meta:
        unique_together = ('character', 'character_owner_hash')
