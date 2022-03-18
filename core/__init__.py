from django.apps import AppConfig
from django.conf import settings

from core.helpers import get_bearer_token

default_app_config = "core.CoreConfig"


class CoreConfig(AppConfig):
    name = "core"

    def ready(self):
        settings.BEARER_TOKEN = get_bearer_token()
