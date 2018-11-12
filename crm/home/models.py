from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    """客户表"""
    name = models.CharField(max_length=32, blank=True, null=True)
    # 客户名称，最多32个字节，blank可以在admin中为空，null可以在数据库中为空
    qq = models.CharField(max_length=64, unique=True)  # qq
    qq_name = models.CharField(max_length=64, blank=True, null=True)  # qq昵称
    phone = models.CharField(max_length=64, blank=True, null=True)  # 手机号
    # 联系方式，最多64字节
    source_choices = ((0, '转介绍'),
                      (1, 'QQ群'),
                      (2, '官网'),
                      (3, '百度推广'),
                      (4, '51CTO'),
                      (5, '知乎'),
                      (6, '市场推广'))  # 来源选择
    source = models.SmallIntegerField(choices=source_choices)
    # 客户来源
    referral_from = models.CharField(verbose_name='转介绍人', max_length=64, blank=True, null=True)
    # 转介绍人
    consult_course = models.ForeignKey('Course', verbose_name='咨询课程')
    # 咨询课程, 外键关联课程表
    content = models.TextField(verbose_name='咨询详情')
    # 咨询详情, 必填
    consultant = models.ForeignKey('UserProfile')  # 咨询销售, 课程顾问
    tags = models.ManyToManyField('Tag', blank=True, null=True)  # 标签
    status_choices = ((0, '已报名'),
                      (1, '未报名'),)  # 客户状态选择
    status = models.SmallIntegerField(choices=status_choices, default=1)  # 客户状态
    memo = models.TextField(blank=True, null=True)  # 备注  memo(备忘录)
    date = models.DateTimeField(auto_now_add=True)  # 时间, auto_now_add, 创建该记录时自动添加当前本地时间

    def __str__(self):
        return self.qq

    class Meta:
        verbose_name = '客户表'
        verbose_name_plural = verbose_name


class Tag(models.Model):
    """标签表"""
    name = models.CharField(unique=True, max_length=32)  # 标签名

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '客户状态标签表'
        verbose_name_plural = verbose_name


class CustomerFollowUp(models.Model):
    """客户跟进表"""
    customer = models.ForeignKey('Customer')  # 跟进的客户, 外键关联Customer表
    content = models.TextField(verbose_name='跟进内容')  # 跟进内容
    consultant = models.ForeignKey('UserProfile')  # 跟进人
    intention_choices = ((0, '两周内报名'),
                         (1, '一个月内报名'),
                         (2, '近期无报名计划'),
                         (3, '已在其他机构报名'),
                         (4, '已报名'),
                         (5, '已拉黑'),)  # intention(意向)_choices(选择)
    intention = models.SmallIntegerField(choices=intention_choices)  # (intention)意向
    date = models.DateTimeField(auto_now_add=True)  # 跟进日期, 创建该记录自动添加当前本地时间

    def __str__(self):
        return '{},{}'.format(self.customer.qq, self.intention)  # 返回客户的联系方式和意向(intention)

    class Meta:
        verbose_name = '客户跟进表'
        verbose_name_plural = verbose_name


class Course(models.Model):
    """课程表"""
    name = models.CharField(max_length=64, unique=True)  # 课程名
    price = models.PositiveSmallIntegerField()  # 学费, 字段选项为正数两字节
    period = models.PositiveSmallIntegerField(verbose_name='周期(月)')  # 周期,
    outline = models.TextField()  # 课程大纲

    def __str__(self):
        return self.name  # 返回课程名

    class Meta:
        verbose_name = '课程表'
        verbose_name_plural = verbose_name


class Branch(models.Model):
    """校区表"""
    name = models.CharField(max_length=128, unique=True)  # 校区名
    address = models.CharField(max_length=128)  # 校区地址

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '校区表'
        verbose_name_plural = verbose_name


class ClassList(models.Model):
    """班级表"""
    branch = models.ForeignKey('Branch')  # 外键关联校区表
    course = models.ForeignKey('Course')  # 外键关联课程

    class_type_choices = ((0, '面授(脱产)'),
                          (1, '面授(周末)'),
                          (2, '网络班'))
    class_type = models.SmallIntegerField(choices=class_type_choices, verbose_name='班级类型')

    semester = models.PositiveIntegerField(verbose_name='学期')  # 第几学期
    teachers = models.ManyToManyField('UserProfile')  # 讲师
    start_date = models.DateField(verbose_name='开班日期')
    end_date = models.DateField(verbose_name='结业日期', blank=True, null=True)

    def __str__(self):
        # 返回校区名, 课程名, 学期
        return '{},{},{}'.format(self.branch, self.course, self.semester)

    class Meta:
        unique_together = ('branch', 'course', 'semester')  # 联合唯一约束
        verbose_name = '班级信息表'
        verbose_name_plural = verbose_name


class CourseRecord(models.Model):
    """上课记录表"""
    from_class = models.ForeignKey('ClassList', verbose_name='班级')  # 来自哪个班级, 外键关联ClassList
    day_num = models.PositiveIntegerField(verbose_name='第几节(天)')
    teacher = models.ForeignKey('UserProfile')  # 讲师
    has_homework = models.BooleanField(default=True)  # 有或没有作业
    homework_title = models.CharField(max_length=128, blank=True, null=True)  # 作业的标题, 可以为空
    homework_content = models.TextField(blank=True, null=True)  # 作业的内容, 可以为空
    outline = models.TextField(verbose_name='本节课程大纲')  # 本节课的大纲
    date = models.DateField(auto_now_add=True)  # 时间, 自增

    def __str__(self):
        # 返回班级和课程节数
        return '{}, {}'.format(self.from_class, self.day_num)

    class Meta:
        unique_together = ('from_class', 'day_num')
        verbose_name = '上课记录表'
        verbose_name_plural = verbose_name


class StudyRecord(models.Model):
    """学习记录"""
    student = models.ForeignKey('Enrollment')  # 学生列, 外键关联报名表
    course_record = models.ForeignKey('CourseRecord')  # 上课记录, 外键关联上课记录表
    attendance_choices = ((0, '已签到'),
                          (1, '迟到'),
                          (2, '缺勤'),
                          (3, '早退'),)  # 出勤选项
    attendance = models.PositiveIntegerField(choices=attendance_choices, default=0)  # 出勤状况, 默认签到
    score_choices = ((100, 'A+'),
                     (90, "A"),
                     (85, 'B+'),
                     (80, 'B'),
                     (75, 'B-'),
                     (70, 'C+'),
                     (60, 'C'),
                     (40, 'C-'),
                     (-50, 'D'),
                     (-100, 'COPY'),
                     (0, 'N/A'))  # 成绩选项
    score = models.PositiveIntegerField(choices=score_choices, default=0)  # 学生成绩, 默认N/A
    memo = models.TextField(blank=True, null=True)  # 备注
    date = models.DateField(auto_now_add=True)  # 日期

    def __str__(self):
        # 返回学生, 上课记录, 成绩
        return '{},{},{}'.format(self.student, self.course_record, self.score)

    class Meta:
        unique_together = ('student', 'course_record')  # 学生和上课记录联合唯一
        verbose_name = '学习记录表'
        verbose_name_plural = verbose_name


class Enrollment(models.Model):
    """报名表"""
    customer = models.ForeignKey('Customer', verbose_name='学生')  # 学生信息, 外键关联客户表
    enrolled_class = models.ForeignKey('ClassList', verbose_name='所报课程')  # 所报课程, 关联ClassList表
    consultant = models.ForeignKey('UserProfile', verbose_name='课程顾问')  # 签单销售
    contract_agreed = models.BooleanField(default=False, verbose_name='学员已同意合同条款')
    contract_approved = models.BooleanField(default=False, verbose_name='合同已审核')
    date = models.DateTimeField(auto_now_add=True)  # 报名日期

    def __str__(self):
        return '{} {}'.format(self.customer, self.enrolled_class)

    class Meta:
        unique_together = ('customer', 'enrolled_class')  # 学生和班级联合唯一, 一个学生只能报一个这个班
        verbose_name = '报名表(学生表)'
        verbose_name_plural = verbose_name


class Payment(models.Model):
    """缴费记录"""
    customer = models.ForeignKey('Customer')  # 缴费人
    course = models.ForeignKey('Course', verbose_name='所报课程')  # 所报课程
    amount = models.PositiveIntegerField(verbose_name='数额', default=500)  # 缴费金额
    consultant = models.ForeignKey('UserProfile')  # 办理人
    date = models.DateTimeField(auto_now_add=True)  # 日期

    def __str__(self):
        # 返回缴费人和缴费金额
        return '{} {}'.format(self.customer, self.amount)

    class Meta:
        verbose_name = '缴费记录表'
        verbose_name_plural = verbose_name


class UserProfile(models.Model):
    """账号表"""
    user = models.OneToOneField(User)  # 一对一关联User表
    name = models.CharField(max_length=32)  # 姓名
    role = models.ManyToManyField('Role', blank=True, null=True)  # 角色(也代表权限)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = '账户表'
        verbose_name_plural = verbose_name


class Role(models.Model):
    """角色表"""
    name = models.CharField(max_length=32, unique=True)
    menus = models.ManyToManyField('Menu', blank=True)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = '角色表'
        verbose_name_plural = verbose_name


class Menu(models.Model):
    """菜单"""
    name = models.CharField(max_length=32)
    url_name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '菜单表'
        verbose_name_plural = verbose_name
