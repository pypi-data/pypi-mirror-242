from django.urls import path

from dashboard import views

class DashboardSite:
    def __init__(self):
        self._registry = {}

    def register(self, dashboard_cls):
        dashboard_name = dashboard_cls.__name__
        if dashboard_name in self._registry:
            raise ValueError(f"Dashboard already registered: {dashboard_name}")

        self._registry[dashboard_name] = dashboard_cls

    def get_dashboard(self, name):
        return self._registry.get(name)

    def get_registered_dashboards(self):
        return self._registry

    def get_urls(self):
        urlpatterns = []
        for name, dashboard_cls in self._registry.items():
            urlpatterns.append(
                path(f'{name}/', views.dashboard_view, kwargs={'dashboard_name': name}, name=f'dashboard_{name}')
            )
        return urlpatterns


dashboard_site = DashboardSite()
