from self_admin.sites import site
from students import models


class TestAdmin(object):
    list_display = ['name']


site.register(models.Test, TestAdmin)
