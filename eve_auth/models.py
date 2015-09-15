from django.db import models
from django.conf import settings


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
