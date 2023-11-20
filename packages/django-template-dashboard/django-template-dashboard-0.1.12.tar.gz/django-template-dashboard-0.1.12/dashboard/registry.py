class DashboardRegistry:
    def __init__(self):
        self._registry = {}

    def register(self, dashboard_cls):
        self._registry[dashboard_cls.__name__] = dashboard_cls

    def get_registered_dashboards(self):
        return self._registry


dashboard_registry = DashboardRegistry()
