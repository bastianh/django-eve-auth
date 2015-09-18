from django.contrib import admin
from django.contrib.admin import register

from eve_auth.models import ApiKey, ApiCall, Character, Corporation, Alliance

admin.site.register(Character)
admin.site.register(Corporation)
admin.site.register(Alliance)


@register(ApiCall)
class EveApiCallAdmin(admin.ModelAdmin):
    readonly_fields = ('apikey', 'success', 'path', 'params', 'result_timestamp', 'result_expires',
                       'api_error_code', 'api_error_message', 'http_error_code', 'http_error_message')
    list_display = ('created', 'apikey', 'path', 'success', 'http_error_code', 'api_error_code')
    pass


@register(ApiKey)
class EveApiKeyAdmin(admin.ModelAdmin):
    list_display = ('key_id', 'key_type', 'owner', 'status', 'status_changed', 'deleted')
    list_display_links = ('key_id',)
    list_filter = ('key_type', 'deleted', 'status')

    readonly_fields = ('key_id', 'key_type', 'characters', 'status', 'status_changed',
                       'corporation', 'updated', 'expires', 'access_mask')

    ordering = ('status_changed',)
