from home import models
from self_admin.sites import site
from self_admin.admin_base import BaseSelfAdmin


class CustomerAdmin(BaseSelfAdmin):
    """客户后台管理"""
    list_display = ('id', 'qq', 'source', 'consultant', 'status', 'content', 'date')
    list_filter = ('source', 'consultant', 'date', 'status')
    search_fields = ('qq', 'name')
    raw_id_fields = ('consult_course',)
    filter_horizontal = ('tags',)
    list_editable = ('status',)


site.register(models.Customer, CustomerAdmin)
# site.register(models.Role, CustomerAdmin)
# site.register(models.UserProfile, CustomerAdmin)
