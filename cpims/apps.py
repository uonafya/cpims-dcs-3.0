"""Main configurations information."""
from django.apps import AppConfig


class AuthAppConfig(AppConfig):
    """Details for authentication module."""

    name = 'cpovc_auth'
    verbose_name = 'User Management'


class MainAppConfig(AppConfig):
    """Details for common application module."""

    name = 'cpovc_main'
    verbose_name = 'System Lookups and Settings'


class RegAppConfig(AppConfig):
    """Details for Registry modules."""

    name = 'cpovc_registry'
    verbose_name = 'Registry Management'


class AccessAppConfig(AppConfig):
    """Details for Registry modules."""

    name = 'cpovc_access'
    verbose_name = 'Access Management'


class FormsAppConfig(AppConfig):
    """docstring for FormsAppConfig"""

    name = 'cpovc_forms'
    verbose_name = 'Forms Management'


class RegReportConfig(AppConfig):
    """docstring for FormsAppConfig"""

    name = 'cpovc_reports'
    verbose_name = 'Reports Management'


class RegHelpConfig(AppConfig):
    """docstring for FormsAppConfig"""

    name = 'cpovc_help'
    verbose_name = 'Help, FAQ and Documentation'
