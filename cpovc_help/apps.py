"""Accessp app with password policies."""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class HelpAppConfig(AppConfig):
    """Password policies."""

    name = 'cpovc_help'
    verbose_name = _('Help')
