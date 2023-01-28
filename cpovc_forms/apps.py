"""Accessp app with password policies."""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FormsAppConfig(AppConfig):
    """Password policies."""

    name = 'cpovc_forms'
    verbose_name = _('Forms')
