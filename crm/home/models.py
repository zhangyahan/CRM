from django.db import models


class Customer(models.Model):
    """客户表"""
    name = models.CharField(max_length=32, blank=True, null=True)
    # 客户名称，最多32个字节，blank可以在admin中为空，null可以在数据库中为空
    contact = models.CharField(max_length=64, unique=True)
    # 联系方式，最多64位，不可以为空


class CustomerFollowUp(models.Model):
    """客户跟进表"""
    pass


class Course(models.Model):
    """课程表"""
    pass


class ClassList(models.Model):
    """班级表"""
    pass


class CourseRecord(models.Model):
    """上课记录表"""
    pass


class StudyRecord(models.Model):
    """学习记录"""
    pass


class Enrollment(models.Model):
    """报名表"""
    pass


class UserProfile(models.Model):
    """账号表"""
    pass


class Role(models.Model):
    """角色表"""
    pass
