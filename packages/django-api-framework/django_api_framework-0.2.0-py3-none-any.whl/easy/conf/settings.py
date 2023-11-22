from typing import Any

from django.conf import settings as django_settings
from django.test.signals import setting_changed

# AUTO ADMIN API settings
# If not all
CRUD_API_ENABLED_ALL_APPS = getattr(django_settings, "CRUD_API_ENABLED_ALL_APPS", True)
# Only generate for included apps
CRUD_API_INCLUDE_APPS = getattr(django_settings, "CRUD_API_INCLUDE_APPS", [])
# Exclude apps always got excluded
CRUD_API_EXCLUDE_APPS = getattr(django_settings, "CRUD_API_EXCLUDE_APPS", [])


def reload_settings(*args: Any, **kwargs: Any) -> None:  # pragma: no cover
    global settings

    setting, value = kwargs["setting"], kwargs["value"]
    globals()[setting] = value


setting_changed.connect(reload_settings)  # pragma: no cover
