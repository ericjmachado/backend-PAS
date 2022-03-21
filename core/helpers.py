import base64
from django.conf import settings
import requests
from django.utils import timezone


def generate_base64_token(key, password):
    token = base64.b64encode(bytes(f"{key}:{password}", "utf-8")).decode("utf-8")
    return f"Basic {token}"


def get_bearer_token():
    basic = settings.BASIC_TOKEN
    headers = {"Authorization": basic}
    data = {"grant_type": "client_credentials"}
    response = requests.post(
        f"{settings.URL_UFG_API}/token", headers=headers, data=data, verify=False
    )
    token = response.json().get("access_token")
    return f"Bearer {token}"


def get_bearer_token_from_updated():
    def _default_setup():
        settings.BEARER_TOKEN = get_bearer_token()
        settings.BEARER_REFRESH_AT = timezone.now()
        return settings.BEARER_TOKEN

    refreshed_at = settings.BEARER_REFRESH_AT
    if refreshed_at is not None:
        if (timezone.now() - refreshed_at).seconds > 3600:
            return _default_setup()
        else:
            return settings.BEARER_TOKEN
    else:
        return _default_setup()
