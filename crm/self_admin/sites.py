from self_admin.admin_base import BaseSelfAdmin


class AdminSite(object):
    def __init__(self):
        self.enabled_admins = {}

    def register(self, model_class, admin_class=BaseSelfAdmin):
        """注册admin表"""
        app_name = model_class._meta.app_label
        model_name = model_class._meta.model_name
        admin_class.model = model_class  # 把model_class赋值给admin_class
        if app_name not in self.enabled_admins:
            self.enabled_admins[app_name] = {}
        self.enabled_admins[app_name][model_name] = admin_class

        print(model_class._meta.app_label, admin_class)


site = AdminSite()
