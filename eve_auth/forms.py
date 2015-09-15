from django.forms import ModelForm
from eve_auth.models import EveApiKey


class EveApiKeyForm(ModelForm):
    class Meta:
        model = EveApiKey
        fields = ['key_id', 'vcode']
