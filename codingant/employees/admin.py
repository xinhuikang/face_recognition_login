from django.contrib import admin
from django.contrib.admin import ModelAdmin, SimpleListFilter
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html
from suit_redactor.widgets import RedactorWidget
from employees.models import Resume, Education, WorkExperience, Project, Certification, Skill, Interview, Activity, \
    Employee, IdCard, Card, ContactPerson, Comment, TrainingExperience, InterviewResume, Salary, WorkProject, \
    Meeting, WorkReport, UserWorkProject, TimeSheet
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from import_export import resources

def get_full_name(self):
    return '%s%s' % (self.last_name, self.first_name)


User.__str__ = get_full_name


class ActivityAdminForm(ModelForm):
    class Meta:
        model = Activity
        fields = ['user', 'content']


class ActivityAdmin(ModelAdmin):
    list_display = ['user', 'activity_date', 'content', 'update_time']
    list_display_links = list_display
    list_filter = ['user']
    ordering = ['-activity_date']

    fields = ['user', 'activity_date', 'content']
    form = ActivityAdminForm
    autocomplete_fields = ['user']

    def save_model(self, request, obj, form, change):
        obj.updater = request.user
        if not change:
            obj.creator = request.user
        super().save_model(request, obj, form, change)


class MyUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', )


class MyUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined']
    list_display_links = list_display
    ordering = ['-date_joined']

    add_form = MyUserCreationForm
    prepopulated_fields = {'username': ('first_name', 'last_name', )}

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'username', 'password1', 'password2', ),
        }),
    )


class InterviewResumeAdmin(ModelAdmin):
    list_display = ['user', 'telephone', 'email', 'view_resume']
    list_display_links = None
    list_filter = ['user']

    def view_resume(self, obj):
        return format_html('<a href="{}" target="_blank">查看简历</a>', reverse('interview_resume', args=(obj.user.pk,)))

    view_resume.allow_tags = True
    view_resume.short_description = '查看简历'


class InterviewDoneFilter(SimpleListFilter):
    title = '是否已经面试'
    parameter_name = 'done'

    def lookups(self, request, model_admin):
        return ('true', '已面试'), ('false', '未面试')

    def queryset(self, request, queryset):
        if self.value() == 'true':
            return queryset.filter(time__lt=timezone.now())
        if self.value() == 'false':
            return queryset.filter(time__gt=timezone.now())


class InterviewAdmin(ModelAdmin):
    list_display = ['user', 'time', 'interviewer', 'result', 'view_resume']
    list_display_links = ['user', 'time', 'interviewer', 'result']
    ordering = ['-time']
    list_filter = ['user', InterviewDoneFilter]

    autocomplete_fields = ['user']
    change_form_template = 'admin/change_form_more_time.html'

    def view_resume(self, obj):
        return format_html('<a type="button" class="btn btn-primary" href="{}" target="_blank">查看简历</a>', reverse('interview_resume', args=(obj.user.pk,)))

    view_resume.allow_tags = True
    view_resume.short_description = '查看简历'


class EmployeeStatusFilter(admin.SimpleListFilter):
    title = '是否在职'
    parameter_name = 'employee_status'

    def lookups(self, request, model_admin):
        return ('false', '离职'), ('true', '在职')

    def queryset(self, request, queryset):
        if self.value() == 'false':
            return queryset.filter(status__in=[2])
        if self.value() == 'true':
            return queryset.filter(status__in=[1, 3, 4])


class EmployeeAdmin(ModelAdmin):
    list_display = ['user', 'number', 'type', 'status', 'enter_date', 'qualify_date', 'leave_date', 'view_info']
    list_display_links = list_display

    autocomplete_fields = ['user']
    ordering = ['-enter_date']
    list_filter = ['type', 'status', EmployeeStatusFilter]

    def view_info(self, obj):
        return format_html('<a type="button" class="btn btn-primary" href="{}" target="_blank">查看资料</a>', reverse('interview_resume', args=(obj.user.pk,)))

    view_info.allow_tags = True
    view_info.short_description = '查看资料'


class WorkProjectAdmin(ModelAdmin):
    list_display = ('identify', 'short_name', 'start_time', 'end_time')
    list_display_links = list_display
    list_filter = ['start_time', 'end_time']
    search_fields = ['name']
    ordering = ('-start_time',)



class SalaryAdmin(ModelAdmin):
    list_display = ('user', 'salary_level', 'salary_proportion', 'gross_salary', 'actual_salary')
    list_display_links = list_display
    autocomplete_fields = ['user']
    list_filter = ['salary_level']

    change_form_template = 'admin/change_form_salary.html'


class WorkReportAdmin(ModelAdmin):
    # form = DailyReportForm
    list_display = ('user', 'header', 'create_time')
    list_display_links = list_display
    autocomplete_fields = ['user']
    list_filter = ['create_time', 'score']
    formfield_overrides = {
        models.TextField: {'widget': RedactorWidget(editor_options={'lang': 'en', 'minHeight': '200'})}
    }

    fieldsets = (
        [None, {
            'fields': ('user', 'header', 'create_time', 'report_content'),
        }],
        ['评价', {
            'fields': ('assess', 'score',),
        }],
    )


class RegularMeetingAdmin(ModelAdmin):
    # form = RegularMeetingForm
    list_display = ('speaker', 'title', 'meeting_time')
    list_display_links = list_display
    autocomplete_fields = ['speaker']
    list_filter = ['speaker', 'meeting_time']
    formfield_overrides = {
        models.TextField: {'widget': RedactorWidget(editor_options={'lang': 'en', 'minHeight': '200'})}
    }


class UserWorkProjectAdmin(ModelAdmin):
    list_display = ('user', 'work_project', 'create_time', 'end_time')
    list_display_links = list_display
    autocomplete_fields = ['user', 'work_project']
    list_filter = ['user', 'work_project__short_name']


class TimeSheetResource(resources.ModelResource):
    class Meta:
        model = TimeSheet
        skip_unchanged = True  # 导入数据时，如果该条数据未修改过，则会忽略（默认根据id去匹配数据，可通过定义import_id_fields去更改）
        exclude = ('user', 'alert_user', 'create_user', 'create_time',
                    'alert_time', 'id',)
        export_order = ('work_project', 'year', 'month',
                    'time_percentage', )


class LaborTimeAdmin(ImportExportModelAdmin,ModelAdmin):
    list_display = ('user', 'work_project', 'year', 'month',
                    'time_percentage', 'create_user', 'create_time',
                    'alert_user', 'alert_time')
    list_display_links = list_display
    autocomplete_fields = ['user', 'work_project', 'create_user', 'alert_user']
    list_filter = ['year', 'month', 'user', 'work_project__short_name', ]
    resource_class = TimeSheetResource

    def save_model(self, request, obj, form, change):
        obj.alert_user = request.user
        obj.create_user = request.user
        obj.save()



admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
admin.site.register(Resume)
admin.site.register(InterviewResume, InterviewResumeAdmin)
admin.site.register(Education)
admin.site.register(WorkExperience)
admin.site.register(Project)
admin.site.register(Certification)
admin.site.register(Skill)
admin.site.register(Interview, InterviewAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(IdCard)
admin.site.register(Card)
admin.site.register(ContactPerson)
admin.site.register(Comment)
admin.site.register(TrainingExperience)
admin.site.register(Salary, SalaryAdmin)
admin.site.register(WorkProject, WorkProjectAdmin)
admin.site.register(WorkReport, WorkReportAdmin)
admin.site.register(Meeting, RegularMeetingAdmin)
admin.site.register(UserWorkProject, UserWorkProjectAdmin)
admin.site.register(TimeSheet, LaborTimeAdmin)

