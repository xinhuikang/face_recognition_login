from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from employees.utils import calculate_age


def get_full_name(self):
    return '%s%s' % (self.last_name, self.first_name)


User.__str__ = get_full_name


class Resume(models.Model):
    GENDER_CHOICES = (
        (1, '男'),
        (2, '女')
    )
    MARITAL_CHOICES = (
        (1, '单身'),
        (2, '恋爱中'),
        (3, '已婚'),
        (4, '离异'),
        (5, '其他')
    )
    ENGLISH_LEVEL_CHOICES = (
        (1, 'CET4'),
        (2, 'CET6'),
        (6, 'CET3'),
        (3, 'IELTS'),
        (4, 'TOEFL'),
        (5, '其他')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')

    gender = models.IntegerField(choices=GENDER_CHOICES, verbose_name='性别')
    # TODO change to select type
    native_place = models.CharField(max_length=100, verbose_name='籍贯')
    # TODO change to select type
    nationality = models.CharField(max_length=100, verbose_name='民族')
    birth_date = models.DateField(verbose_name='出生日期', help_text='以身份证为准')
    marital_status = models.IntegerField(choices=MARITAL_CHOICES, verbose_name='婚姻状况')

    # TODO change to select type
    target_position = models.CharField(max_length=100, verbose_name='求职意向')
    expect_salary = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='期望薪水（转正后）')
    expect_salary_intern = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2, verbose_name='期望薪水（实习期）')

    telephone = models.CharField(max_length=100, verbose_name='联系电话')
    email = models.EmailField(verbose_name='电子邮箱地址')
    qq = models.CharField(max_length=100, verbose_name='QQ号码')
    wechat = models.CharField(max_length=100, blank=True, null=True, verbose_name='微信号')

    english_level = models.IntegerField(choices=ENGLISH_LEVEL_CHOICES, verbose_name='英语证书最高等级')
    english_score = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name='英语证书最高成绩')

    height = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name='身高', help_text='单位：cm')
    weight = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name='体重', help_text='单位：公斤')

    introduction = models.TextField(verbose_name='自我评价')
    is_submitted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.__str__() + '个人简历'

    class Meta:
        verbose_name = '基本信息'
        verbose_name_plural = verbose_name

    @property
    def age(self):
        return calculate_age(timezone.now().date(), self.birth_date)


class InterviewResume(Resume):
    class Meta:
        proxy = True
        verbose_name = '人员简历'
        verbose_name_plural = verbose_name


class Education(models.Model):
    EDUCATION_CHOICES = (
        (1, '本科'),
        (2, '专科'),
        (3, '硕士'),
        (4, '博士'),
        (5, '其他')
    )
    EDUCATION_TYPE_CHOICES = (
        (1, '全日制'),
        (2, '非全日制'),
        (3, '自考'),
        (4, '专升本'),
        (5, '其他')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    school = models.CharField(max_length=100, verbose_name='学校名称')
    major = models.CharField(max_length=100, verbose_name='专业')
    education = models.IntegerField(choices=EDUCATION_CHOICES, verbose_name='学历')
    education_type = models.IntegerField(choices=EDUCATION_TYPE_CHOICES, verbose_name='学历类型')
    # TODO change to year and month
    start_date = models.DateField(verbose_name='开始时间')
    end_date = models.DateField(blank=True, null=True, verbose_name='结束时间')

    def __str__(self):
        return self.school + self.get_education_type_display() + self.get_education_display()

    class Meta:
        verbose_name = '教育经历'
        verbose_name_plural = verbose_name


class WorkExperience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    company_name = models.CharField(max_length=100, verbose_name='单位名称')
    position = models.CharField(max_length=100, verbose_name='职位/岗位')
    description = models.TextField(verbose_name='工作内容描述')
    resignation_reason = models.CharField(max_length=1000, verbose_name='离职原因')
    start_date = models.DateField(verbose_name='开始时间')
    end_date = models.DateField(blank=True, null=True, verbose_name='结束时间')

    def __str__(self):
        return self.company_name + self.position

    class Meta:
        verbose_name = '工作经历'
        verbose_name_plural = verbose_name


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=100, verbose_name='项目名称')
    description = models.TextField(verbose_name='项目描述')
    technology = models.TextField(verbose_name='技术要点描述')
    responsibility = models.TextField(verbose_name='个人负责工作')

    start_date = models.DateField(verbose_name='开始时间')
    end_date = models.DateField(blank=True, null=True, verbose_name='结束时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '项目经历'
        verbose_name_plural = verbose_name


class Certification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=100, verbose_name='获奖/证书名称')
    remark = models.CharField(max_length=1000, blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '获奖/证书情况'
        verbose_name_plural = verbose_name


class Skill(models.Model):
    LEVEL_CHOICES = (
        (1, '熟练'),
        (2, '掌握'),
        (3, '熟悉'),
        (4, '了解')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    level = models.IntegerField(choices=LEVEL_CHOICES, verbose_name='技能水平')
    content = models.CharField(max_length=100, verbose_name='技能描述')

    def __str__(self):
        return self.get_level_display() + self.content

    class Meta:
        verbose_name = '技能水平'
        verbose_name_plural = verbose_name


class Interview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='应聘人')

    interviewer = models.CharField(max_length=100, verbose_name='面试官')
    written_test_score = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name='笔试成绩')
    interview_score = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name='面试成绩')
    comment = models.TextField(blank=True, null=True, verbose_name='面试评语')
    result = models.TextField(blank=True, null=True, verbose_name='面试结果')

    time = models.DateTimeField(verbose_name='面试时间')

    def __str__(self):
        return self.user.__str__() + '的面试'

    class Meta:
        verbose_name = '面试情况'
        verbose_name_plural = verbose_name


class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')

    create_time = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_creator')
    update_time = models.DateTimeField(auto_now=True)
    updater = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_updater', blank=True, null=True)

    activity_date = models.DateField(verbose_name='日期')
    content = models.CharField(max_length=1000, verbose_name='动态')

    class Meta:
        verbose_name = '人员动态'
        verbose_name_plural = '人员动态'

    def __str__(self):
        return self.user.last_name + self.user.first_name + self.activity_date.strftime("%Y年%m月%d日") + self.content


class Employee(models.Model):
    EMPLOYEE_TYPE_CHOICES = (
        (1, '正式员工'),
        (2, '实习生'),
        (3, '研究生'),
        (4, '培训生'),
        (5, '其他')
    )
    EMPLOYEE_STATUS_CHOICES = (
        (1, '已转正'),
        (2, '已离职'),
        (3, '试用期'),
        (4, '其他'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='姓名')

    number = models.CharField(max_length=100, verbose_name='工号', help_text='正式员工工号以1开头，实习生以2开头，研究生以3开头，培训生以4开头，其他人以5开头，长度暂定5位')
    type = models.IntegerField(choices=EMPLOYEE_TYPE_CHOICES, verbose_name='员工类型')
    status = models.IntegerField(choices=EMPLOYEE_STATUS_CHOICES, verbose_name='员工状态')
    is_submitted = models.BooleanField(default=False)
    enter_date = models.DateField(verbose_name='入职日期')
    qualify_date = models.DateField(blank=True, null=True, verbose_name='转正日期')
    leave_date = models.DateField(blank=True, null=True, verbose_name='离职日期')

    def __str__(self):
        return self.number + self.user.__str__()

    class Meta:
        verbose_name = '员工信息'
        verbose_name_plural = verbose_name


class IdCard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    id_card_number = models.CharField(max_length=18, verbose_name='身份证号')
    residence_address = models.CharField(max_length=1000, verbose_name='居住地')
    id_card_address = models.CharField(max_length=100, verbose_name='身份证上的住址')
    id_card_photo = models.ImageField(upload_to='profile', verbose_name='身份证正反面扫描图')

    def __str__(self):
        return self.user.__str__() + '的身份证'

    class Meta:
        verbose_name = '身份证信息'
        verbose_name_plural = verbose_name


class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    number = models.CharField(max_length=100, verbose_name='银行卡号')
    bank_name = models.CharField(max_length=100, verbose_name='银行名称')
    branch_name = models.CharField(max_length=100, verbose_name='开户行')
    phone = models.CharField(max_length=100, verbose_name='银行预留手机号码')
    is_default = models.BooleanField(verbose_name='是否默认银行卡')
    remark = models.TextField(verbose_name='备注', blank=True, null=True)

    def __str__(self):
        return self.user.__str__() + '的' + self.bank_name + '卡'

    class Meta:
        verbose_name = '银行卡信息'
        verbose_name_plural = verbose_name


class ContactPerson(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=100, verbose_name='联系人姓名')
    relationship = models.CharField(max_length=100, verbose_name='关系')
    organization = models.CharField(max_length=1000, verbose_name='工作单位')
    telephone = models.CharField(max_length=100, verbose_name='联系电话')

    def __str__(self):
        return self.name + self.telephone

    class Meta:
        verbose_name = '联系人'
        verbose_name_plural = verbose_name


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    content = models.TextField(verbose_name='评价内容')

    create_time = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_creator')
    update_time = models.DateTimeField(auto_now=True)
    updater = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_updater')

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = '员工评价'
        verbose_name_plural = verbose_name


class TrainingExperience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=1000, verbose_name='培训名称')
    organization_name = models.CharField(max_length=1000, verbose_name='培训机构名称')
    start_date = models.DateField(verbose_name='开始日期')
    end_date = models.DateField(blank=True, null=True, verbose_name='结束日期')

    content = models.TextField(verbose_name='培训内容或收获')

    def __str__(self):
        return self.name + '|' + self.organization_name

    class Meta:
        verbose_name = '培训经历'
        verbose_name_plural = verbose_name


class WorkProject(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=500, verbose_name='项目名称')
    identify = models.CharField(max_length=500, verbose_name='项目编号')
    short_name = models.CharField(max_length=500, verbose_name='项目简称')
    description = models.TextField(verbose_name='项目描述')
    key_skill = models.TextField(verbose_name='技术要点')
    start_time = models.DateField(verbose_name='开始日期')
    end_time = models.DateField(blank=True, null=True, verbose_name='结束日期')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '公司项目信息'
        verbose_name_plural = verbose_name


class Salary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    salary_level = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='工资标准')
    salary_proportion = models.DecimalField(max_digits=3, decimal_places=2, verbose_name='工资比例', help_text='填写以1为基准的加成，例如：1.20')
    gross_salary = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='应发工资')
    actual_salary = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='实发工资')

    def __str__(self):
        return self.user.__str__() + '的工资'

    class Meta:
        verbose_name = '工资信息'
        verbose_name_plural = verbose_name


class WorkReport(models.Model):
    SCORE_CHOICES = (
        (1, '很差'),
        (2, '差'),
        (3, '一般'),
        (4, '好'),
        (5, '很好')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    header = models.CharField(max_length=100, verbose_name='日报标题')
    create_time = models.DateTimeField(verbose_name='时间')
    report_content = models.TextField(verbose_name='日报内容')
    assess = models.TextField(verbose_name='评价内容', blank=True, null=True)
    score = models.IntegerField(choices=SCORE_CHOICES, verbose_name='评价等级', blank=True, null=True)

    def __str__(self):
        return self.header

    class Meta:
        verbose_name = '人员报表'
        verbose_name_plural = verbose_name


class Meeting(models.Model):
    # 例会标题，例会参与人员，例会时间，例会主要内容（富文本格式）和附件
    title = models.CharField(max_length=50, verbose_name="例会标题")
    speaker = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="报告人")  # Employee
    participant = models.CharField(max_length=500, verbose_name="参与人员")
    meeting_time = models.DateTimeField(verbose_name="例会时间")
    main_content = models.TextField(verbose_name="例会主要内容")
    enclosure = models.FileField(upload_to='./upload/', verbose_name="附件")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '技术分享'
        verbose_name_plural = verbose_name


class UserWorkProject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    work_project = models.ForeignKey(WorkProject, on_delete=models.CASCADE, verbose_name='项目名称')

    create_time = models.DateField(verbose_name='加入时间', default=timezone.now)
    end_time = models.DateField(verbose_name='退出时间', null=True, blank=True)

    def __str__(self):
        return self.work_project.__str__()

    class Meta:
        verbose_name = '用户和项目'
        verbose_name_plural = verbose_name


class TimeSheet(models.Model):
    MONTHS_CHOICES = (
        (1, '一月'),
        (2, '二月'),
        (3, '三月'),
        (4, '四月'),
        (5, '五月'),
        (6, '六月'),
        (7, '七月'),
        (8, '八月'),
        (9, '九月'),
        (10, '十月'),
        (11, '十一月'),
        (12, '十二月'),
    )
    YEARS_CHOICES = (
        (timezone.now().year - 2017, timezone.now().year - 1),
        (timezone.now().year - 2016, timezone.now().year),
    )
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE, verbose_name='用户')
    work_project = models.ForeignKey(WorkProject, on_delete=models.CASCADE, verbose_name='项目名称')

    year = models.IntegerField(choices=YEARS_CHOICES, verbose_name='年份', default=timezone.now().year - 2016)
    month = models.IntegerField(choices=MONTHS_CHOICES, verbose_name='月份')
    time_percentage = models.SmallIntegerField(verbose_name='时间百分比', help_text='该用户在该项目占用的工作时间比例')

    create_user = models.ForeignKey(User, models.SET_NULL, related_name='create_user', editable=False, null=True, blank=True,
                                    verbose_name='创建者')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    alert_user = models.ForeignKey(User, models.SET_NULL, related_name='alert_user', editable=False, null=True, blank=True, verbose_name='修改者')
    alert_time = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name='修改时间')

    def __str__(self):
        return self.user.__str__() + '的' + self.work_project.__str__() + ' 项目的工时百分比'

    class Meta:
        verbose_name = '月份工时'
        verbose_name_plural = verbose_name
        unique_together = (("user", "year", 'month', 'work_project'),)
