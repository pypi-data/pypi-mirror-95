#
# Copyright 2015, Martin Owens <doctormo@gmail.com>
#
# This file is part of the software inkscape-web, consisting of custom 
# code for the Inkscape project's django-based website.
#
# inkscape-web is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# inkscape-web is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with inkscape-web.  If not, see <http://www.gnu.org/licenses/>.
#
"""
Loads all the alert modules and registers everything when ready.
"""

import re
import sys
from importlib import import_module

from django.apps import AppConfig, apps
from django.utils.module_loading import module_has_submodule
from django.db.models.signals import post_migrate

ALERT_MODULE_NAME = 'alert'
IS_TEST = 'test' in sys.argv or 'autotest' in sys.argv
IS_MIGRATE = 'migrate' in sys.argv or 'makemigrations' in sys.argv

class AlertsConfig(AppConfig):
    name = 'alerts'

    def ready(self):
        from alerts.base import BaseAlert

        for app_config in apps.app_configs.values():
            app = app_config.module
            if module_has_submodule(app, ALERT_MODULE_NAME):
                app = app.__name__
                module = import_module("%s.%s" % (app, ALERT_MODULE_NAME))
                for (name, value) in module.__dict__.items():
                    if type(value) is type(BaseAlert) and \
                         issubclass(value, BaseAlert) and \
                         value.__module__ == module.__name__ and \
                         (not value.test_only or IS_TEST):
                        self.register(app, value)

    def register(self, app, cls):
        name = re.sub('(?!^)([A-Z]+)', r'_\1', cls.__name__)
        slug = "{}.{}".format(app, name)[:32].lower()
        try:
            cls(slug, is_test=IS_TEST, is_migrate=IS_MIGRATE) # Singleton
        except Exception as err:
            if any(cmd in sys.argv for cmd in ['runserver', 'shell']):
                sys.stderr.write("Err in alert: %s\n%s\n" % (slug, str(err)))
            raise

