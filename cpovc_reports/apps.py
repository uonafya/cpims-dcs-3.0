"""Accessp app with password policies."""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ReportsAppConfig(AppConfig):
    """Password policies."""

    name = 'cpovc_reports'
    verbose_name = _('Reports')
