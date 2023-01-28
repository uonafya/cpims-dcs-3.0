"""Accessp app with password policies."""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ManageAppConfig(AppConfig):
    """Password policies."""

    name = 'cpovc_manage'
    verbose_name = _('Manage')
