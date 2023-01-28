"""Accessp app with password policies."""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class GISAppConfig(AppConfig):
    """Password policies."""

    name = 'cpovc_gis'
    verbose_name = _('GIS')
