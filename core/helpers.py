import base64
from django.conf import settings
import requests


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
