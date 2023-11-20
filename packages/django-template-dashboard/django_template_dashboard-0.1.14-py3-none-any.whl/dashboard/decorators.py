from django.apps import apps

from dashboard.sites import dashboard_site


# 定义 register 装饰器
def register(dashboard_cls):
    # 注册 dashboard_cls 到 dashboard_registry
    dashboard_site.register(dashboard_cls)

    # 返回原始的 dashboard_cls
    return dashboard_cls
