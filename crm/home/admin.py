from django.contrib import admin
from .models import *


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """客户后台管理"""
    list_display = ('id', 'qq', 'source', 'consultant', 'status', 'content', 'date')
    list_filter = ('source', 'consultant', 'date')
    search_fields = ('qq', 'name')
    raw_id_fields = ('consult_course',)
    filter_horizontal = ('tags',)
    list_editable = ('status',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """标签后台管理"""
    pass


@admin.register(CustomerFollowUp)
class CustomerFollowUpAdmin(admin.ModelAdmin):
    """客户跟进后台管理"""
    pass


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """课程后台管理"""
    pass


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    """校区后台管理"""
    pass


@admin.register(ClassList)
class ClassListAdmin(admin.ModelAdmin):
    """班级后台管理"""
    pass


@admin.register(CourseRecord)
class CourseRecordAdmin(admin.ModelAdmin):
    pass


@admin.register(StudyRecord)
class StudyRecordAdmin(admin.ModelAdmin):
    """上课记录后台管理"""
    pass


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    """学习记录后台管理"""
    pass


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """报名客户后台管理"""
    pass


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """账号后台管理"""
    pass


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """角色后台管理"""
    pass


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    """菜单"""
    pass


