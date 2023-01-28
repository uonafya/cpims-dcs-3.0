''' Django notifications apps file '''
# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

import notifications.signals


class NotificationAppConfig(AppConfig):
    """Password policies."""

    name = 'notifications'
    verbose_name = _('System Notifications')

    def ready(self):
        super(NotificationAppConfig, self).ready()
        # this is for backwards compability
        notifications.notify = notifications.signals.notify
