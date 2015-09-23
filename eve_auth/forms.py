from django.forms import ModelForm

from eve_auth.models import ApiKey


class EveApiKeyForm(ModelForm):
    class Meta:
        model = ApiKey
        fields = ['key_id', 'vcode']
