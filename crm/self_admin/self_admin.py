from home import models

enabled_admins = {}


class BaseAdmin(object):
    list_display = []
    list_filter = []


class CustomerAdmin(BaseAdmin):
    list_display = ['qq', 'name', 'source', 'consultant', 'consult_course', 'date']


class CustomerFollowUpAdmin(BaseAdmin):
    pass


def register(model_class, admin_class=None):
    if model_class._meta.app_label not in enabled_admins:
        enabled_admins[model_class._meta.app_label] = {}
        # model.app_lable(获取当前类的app名) model.model_name(获取当前类的表名)
    admin_class.model = model_class  # 绑定model对象和Admin的类
    enabled_admins[model_class._meta.app_label][model_class._meta.model_name] = admin_class


register(models.Customer, CustomerAdmin)
register(models.CustomerFollowUp, CustomerFollowUpAdmin)
