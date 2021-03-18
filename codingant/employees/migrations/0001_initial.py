# Generated by Django 2.1 on 2019-03-26 01:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('activity_date', models.DateField(verbose_name='日期')),
                ('content', models.CharField(max_length=1000, verbose_name='动态')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activity_creator', to=settings.AUTH_USER_MODEL)),
                ('updater', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='activity_updater', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '人员动态',
                'verbose_name_plural': '人员动态',
            },
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=100, verbose_name='银行卡号')),
                ('bank_name', models.CharField(max_length=100, verbose_name='银行名称')),
                ('branch_name', models.CharField(max_length=100, verbose_name='开户行')),
                ('phone', models.CharField(max_length=100, verbose_name='银行预留手机号码')),
                ('is_default', models.BooleanField(verbose_name='是否默认银行卡')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '银行卡信息',
                'verbose_name_plural': '银行卡信息',
            },
        ),
        migrations.CreateModel(
            name='Certification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='获奖/证书名称')),
                ('remark', models.CharField(blank=True, max_length=1000, null=True, verbose_name='备注')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '获奖/证书情况',
                'verbose_name_plural': '获奖/证书情况',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='评价内容')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_creator', to=settings.AUTH_USER_MODEL)),
                ('updater', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_updater', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '员工评价',
                'verbose_name_plural': '员工评价',
            },
        ),
        migrations.CreateModel(
            name='ContactPerson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='联系人姓名')),
                ('relationship', models.CharField(max_length=100, verbose_name='关系')),
                ('organization', models.CharField(max_length=1000, verbose_name='工作单位')),
                ('telephone', models.CharField(max_length=100, verbose_name='联系电话')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '联系人',
                'verbose_name_plural': '联系人',
            },
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school', models.CharField(max_length=100, verbose_name='学校名称')),
                ('major', models.CharField(max_length=100, verbose_name='专业')),
                ('education', models.IntegerField(choices=[(1, '本科'), (2, '专科'), (3, '硕士'), (4, '博士'), (5, '其他')], verbose_name='学历')),
                ('education_type', models.IntegerField(choices=[(1, '全日制'), (2, '非全日制'), (3, '自考'), (4, '专升本'), (5, '其他')], verbose_name='学历类型')),
                ('start_date', models.DateField(verbose_name='开始时间')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='结束时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '教育经历',
                'verbose_name_plural': '教育经历',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(help_text='正式员工工号以1开头，实习生以2开头，研究生以3开头，培训生以4开头，其他人以5开头，长度暂定5位', max_length=100, verbose_name='工号')),
                ('type', models.IntegerField(choices=[(1, '正式员工'), (2, '实习生'), (3, '研究生'), (4, '培训生'), (5, '其他')], verbose_name='员工类型')),
                ('status', models.IntegerField(choices=[(1, '已转正'), (2, '已离职'), (3, '试用期'), (4, '其他')], verbose_name='员工状态')),
                ('is_submitted', models.BooleanField(default=False)),
                ('enter_date', models.DateField(verbose_name='入职日期')),
                ('qualify_date', models.DateField(blank=True, null=True, verbose_name='转正日期')),
                ('leave_date', models.DateField(blank=True, null=True, verbose_name='离职日期')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='姓名')),
            ],
            options={
                'verbose_name': '员工信息',
                'verbose_name_plural': '员工信息',
            },
        ),
        migrations.CreateModel(
            name='IdCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_card_number', models.CharField(max_length=18, verbose_name='身份证号')),
                ('residence_address', models.CharField(max_length=1000, verbose_name='居住地')),
                ('id_card_address', models.CharField(max_length=100, verbose_name='身份证上的住址')),
                ('id_card_photo', models.ImageField(upload_to='profile', verbose_name='身份证正反面扫描图')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '身份证信息',
                'verbose_name_plural': '身份证信息',
            },
        ),
        migrations.CreateModel(
            name='Interview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interviewer', models.CharField(max_length=100, verbose_name='面试官')),
                ('written_test_score', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='笔试成绩')),
                ('interview_score', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='面试成绩')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='面试评语')),
                ('result', models.TextField(blank=True, null=True, verbose_name='面试结果')),
                ('time', models.DateTimeField(verbose_name='面试时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='应聘人')),
            ],
            options={
                'verbose_name': '面试情况',
                'verbose_name_plural': '面试情况',
            },
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='例会标题')),
                ('participant', models.CharField(max_length=500, verbose_name='参与人员')),
                ('meeting_time', models.DateTimeField(verbose_name='例会时间')),
                ('main_content', models.TextField(verbose_name='例会主要内容')),
                ('enclosure', models.FileField(upload_to='./upload/', verbose_name='附件')),
                ('speaker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='报告人')),
            ],
            options={
                'verbose_name': '技术分享',
                'verbose_name_plural': '技术分享',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='项目名称')),
                ('description', models.TextField(verbose_name='项目描述')),
                ('technology', models.TextField(verbose_name='技术要点描述')),
                ('responsibility', models.TextField(verbose_name='个人负责工作')),
                ('start_date', models.DateField(verbose_name='开始时间')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='结束时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '项目经历',
                'verbose_name_plural': '项目经历',
            },
        ),
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.IntegerField(choices=[(1, '男'), (2, '女')], verbose_name='性别')),
                ('native_place', models.CharField(max_length=100, verbose_name='籍贯')),
                ('nationality', models.CharField(max_length=100, verbose_name='民族')),
                ('birth_date', models.DateField(help_text='以身份证为准', verbose_name='出生日期')),
                ('marital_status', models.IntegerField(choices=[(1, '单身'), (2, '恋爱中'), (3, '已婚'), (4, '离异'), (5, '其他')], verbose_name='婚姻状况')),
                ('target_position', models.CharField(max_length=100, verbose_name='求职意向')),
                ('expect_salary', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='期望薪水（转正后）')),
                ('expect_salary_intern', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='期望薪水（实习期）')),
                ('telephone', models.CharField(max_length=100, verbose_name='联系电话')),
                ('email', models.EmailField(max_length=254, verbose_name='电子邮箱地址')),
                ('qq', models.CharField(max_length=100, verbose_name='QQ号码')),
                ('wechat', models.CharField(blank=True, max_length=100, null=True, verbose_name='微信号')),
                ('english_level', models.IntegerField(choices=[(1, 'CET4'), (2, 'CET6'), (6, 'CET3'), (3, 'IELTS'), (4, 'TOEFL'), (5, '其他')], verbose_name='英语证书最高等级')),
                ('english_score', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='英语证书最高成绩')),
                ('height', models.DecimalField(blank=True, decimal_places=2, help_text='单位：cm', max_digits=12, null=True, verbose_name='身高')),
                ('weight', models.DecimalField(blank=True, decimal_places=2, help_text='单位：公斤', max_digits=12, null=True, verbose_name='体重')),
                ('introduction', models.TextField(verbose_name='自我评价')),
                ('is_submitted', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '基本信息',
                'verbose_name_plural': '基本信息',
            },
        ),
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salary_level', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='工资标准')),
                ('salary_proportion', models.DecimalField(decimal_places=2, help_text='填写以1为基准的加成，例如：1.20', max_digits=3, verbose_name='工资比例')),
                ('gross_salary', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='应发工资')),
                ('actual_salary', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='实发工资')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '工资信息',
                'verbose_name_plural': '工资信息',
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField(choices=[(1, '熟练'), (2, '掌握'), (3, '熟悉'), (4, '了解')], verbose_name='技能水平')),
                ('content', models.CharField(max_length=100, verbose_name='技能描述')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '技能水平',
                'verbose_name_plural': '技能水平',
            },
        ),
        migrations.CreateModel(
            name='TimeSheet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(choices=[(2, 2018), (3, 2019)], default=3, verbose_name='年份')),
                ('month', models.IntegerField(choices=[(1, '一月'), (2, '二月'), (3, '三月'), (4, '四月'), (5, '五月'), (6, '六月'), (7, '七月'), (8, '八月'), (9, '九月'), (10, '十月'), (11, '十一月'), (12, '十二月')], verbose_name='月份')),
                ('time_percentage', models.SmallIntegerField(help_text='该用户在该项目占用的工作时间比例', verbose_name='时间百分比')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('alert_time', models.DateTimeField(auto_now=True, null=True, verbose_name='修改时间')),
                ('alert_user', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='alert_user', to=settings.AUTH_USER_MODEL, verbose_name='修改者')),
                ('create_user', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='create_user', to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '月份工时',
                'verbose_name_plural': '月份工时',
            },
        ),
        migrations.CreateModel(
            name='TrainingExperience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000, verbose_name='培训名称')),
                ('organization_name', models.CharField(max_length=1000, verbose_name='培训机构名称')),
                ('start_date', models.DateField(verbose_name='开始日期')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='结束日期')),
                ('content', models.TextField(verbose_name='培训内容或收获')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '培训经历',
                'verbose_name_plural': '培训经历',
            },
        ),
        migrations.CreateModel(
            name='UserWorkProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateField(default=django.utils.timezone.now, verbose_name='加入时间')),
                ('end_time', models.DateField(blank=True, null=True, verbose_name='退出时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '用户和项目',
                'verbose_name_plural': '用户和项目',
            },
        ),
        migrations.CreateModel(
            name='WorkExperience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100, verbose_name='单位名称')),
                ('position', models.CharField(max_length=100, verbose_name='职位/岗位')),
                ('description', models.TextField(verbose_name='工作内容描述')),
                ('resignation_reason', models.CharField(max_length=1000, verbose_name='离职原因')),
                ('start_date', models.DateField(verbose_name='开始时间')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='结束时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '工作经历',
                'verbose_name_plural': '工作经历',
            },
        ),
        migrations.CreateModel(
            name='WorkProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='项目名称')),
                ('identify', models.CharField(max_length=500, verbose_name='项目编号')),
                ('short_name', models.CharField(max_length=500, verbose_name='项目简称')),
                ('description', models.TextField(verbose_name='项目描述')),
                ('key_skill', models.TextField(verbose_name='技术要点')),
                ('start_time', models.DateField(verbose_name='开始日期')),
                ('end_time', models.DateField(blank=True, null=True, verbose_name='结束日期')),
            ],
            options={
                'verbose_name': '公司项目信息',
                'verbose_name_plural': '公司项目信息',
            },
        ),
        migrations.CreateModel(
            name='WorkReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(max_length=100, verbose_name='日报标题')),
                ('create_time', models.DateTimeField(verbose_name='时间')),
                ('report_content', models.TextField(verbose_name='日报内容')),
                ('assess', models.TextField(blank=True, null=True, verbose_name='评价内容')),
                ('score', models.IntegerField(blank=True, choices=[(1, '很差'), (2, '差'), (3, '一般'), (4, '好'), (5, '很好')], null=True, verbose_name='评价等级')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '人员报表',
                'verbose_name_plural': '人员报表',
            },
        ),
        migrations.AddField(
            model_name='userworkproject',
            name='work_project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employees.WorkProject', verbose_name='项目名称'),
        ),
        migrations.AddField(
            model_name='timesheet',
            name='work_project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employees.WorkProject', verbose_name='项目名称'),
        ),
        migrations.CreateModel(
            name='InterviewResume',
            fields=[
            ],
            options={
                'verbose_name': '人员简历',
                'verbose_name_plural': '人员简历',
                'proxy': True,
                'indexes': [],
            },
            bases=('employees.resume',),
        ),
        migrations.AlterUniqueTogether(
            name='timesheet',
            unique_together={('user', 'year', 'month', 'work_project')},
        ),
    ]