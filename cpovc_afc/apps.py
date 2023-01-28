"""Accessp app with password policies."""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AFCAppConfig(AppConfig):
    """Password policies."""

    name = 'cpovc_afc'
    verbose_name = _('Alternative Care')
