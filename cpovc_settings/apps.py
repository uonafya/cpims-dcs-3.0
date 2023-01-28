"""Accessp app with password policies."""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SettingsAppConfig(AppConfig):
    """Password policies."""

    name = 'cpovc_settings'
    verbose_name = _('Settings')
