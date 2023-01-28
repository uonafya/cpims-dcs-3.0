"""Accessp app with password policies."""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CTIPAppConfig(AppConfig):
    """Password policies."""

    name = 'cpovc_ctip'
    verbose_name = _('Counter Trafficking in Persons')
