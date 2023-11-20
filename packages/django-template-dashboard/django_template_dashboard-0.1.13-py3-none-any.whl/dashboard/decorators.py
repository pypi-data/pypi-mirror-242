from django.apps import apps

from registries import dashboard_registry


# 定义 register 装饰器
def register(dashboard_cls):
    # 提取模块名称作为 app 的标签
    module = dashboard_cls.__module__
    app_label = module.split('.')[0]
    app_config = apps.get_app_config(app_label)
    app_name = app_config.name

    # 注册 dashboard_cls 到 dashboard_registry
    dashboard_registry.register(app_name, dashboard_cls)

    # 返回原始的 dashboard_cls
    return dashboard_cls
