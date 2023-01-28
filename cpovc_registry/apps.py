"""Accessp app with password policies."""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RegistryAppConfig(AppConfig):
    """Password policies."""

    name = 'cpovc_registry'
    verbose_name = _('Registries')
