from django.utils.module_loading import autodiscover_modules

from dashboard.base import Dashboard
from dashboard.sites import dashboard_site
from dashboard.decorators import register

__all__ = ['Dashboard', 'register']


def autodiscover():
    autodiscover_modules("dashboard", register_to=dashboard_site)
