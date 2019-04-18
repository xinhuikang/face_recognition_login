from django.contrib import messages, admin
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms import inlineformset_factory, modelform_factory, modelformset_factory
from django.http import Http404
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from employees.constants import EDUCATION_FORMS_PREFIX, WORK_EXPERIENCE_FORMS_PREFIX, PROJECT_FORMS_PREFIX, \
    CERTIFICATION_FORMS_PREFIX, SKILL_FORMS_PREFIX, TRAINING_EXPERIENCE_FORMS_PREFIX, CARD_FORMS_PREFIX, \
    CONTACT_FORMS_PREFIX, TIMESHEET_FORMS_PREFIX
from employees.forms import ResumeForm, EducationForm, EducationFormSetHelper, WorkExperienceForm, \
    WorkExperienceFormSetHelper, ProjectForm, ProjectFormSetHelper, CertificationForm, CertificationFormSetHelper, \
    SkillForm, SkillFormSetHelper, TrainingExperienceForm, TrainingExperienceFormSetHelper, IdCardForm, CardForm, \
    ContactForm, CardFormSetHelper, ContactFormSetHelper, TimeSheetForm, TimeSheetFormSetHelper, ChangepwdForm
from employees.models import Education, WorkExperience, Project, Certification, Skill, TrainingExperience, Card, \
    ContactPerson, TimeSheet, UserWorkProject, WorkProject


def form_in_formset_is_valid(form):
    return not (form.empty_permitted and not form.has_changed()) and form.is_valid()


@login_required
def profile(request):
    EducationFormSet = inlineformset_factory(User, Education, form=EducationForm, extra=1)
    WorkExperienceFormSet = inlineformset_factory(User, WorkExperience, form=WorkExperienceForm, extra=1)
    ProjectFormSet = inlineformset_factory(User, Project, form=ProjectForm, extra=1)
    CertificationFormSet = inlineformset_factory(User, Certification, form=CertificationForm, extra=1)
    SkillFormSet = inlineformset_factory(User, Skill, form=SkillForm, extra=2)
    TrainingExperienceFormSet = inlineformset_factory(User, TrainingExperience, form=TrainingExperienceForm, extra=1)

    if request.method == 'POST':
        return post_profile(CertificationFormSet, EducationFormSet, ProjectFormSet, SkillFormSet,
                            TrainingExperienceFormSet, WorkExperienceFormSet, request)

    elif request.method == 'GET':
        return get_profile(CertificationFormSet, EducationFormSet, ProjectFormSet, SkillFormSet,
                           TrainingExperienceFormSet, WorkExperienceFormSet, request)
    else:
        raise Http404('404')


def get_profile(CertificationFormSet, EducationFormSet, ProjectFormSet, SkillFormSet, TrainingExperienceFormSet,
                WorkExperienceFormSet, request):
    if allow_view_employee_profile(request):
        return redirect('employee_profile')
    if hasattr(request.user, 'resume'):
        form = ResumeForm(instance=request.user.resume)

        if request.user.resume.is_submitted:
            user = request.user
            return render(request, 'employees/profile-view.html', {'user': user})
    else:
        form = ResumeForm()
    education_forms = EducationFormSet(instance=request.user, prefix=EDUCATION_FORMS_PREFIX)
    education_forms_helper = EducationFormSetHelper()
    work_experience_forms = WorkExperienceFormSet(instance=request.user, prefix=WORK_EXPERIENCE_FORMS_PREFIX)
    work_experience_forms_helper = WorkExperienceFormSetHelper()
    project_forms = ProjectFormSet(instance=request.user, prefix=PROJECT_FORMS_PREFIX)
    project_forms_helper = ProjectFormSetHelper()
    certification_forms = CertificationFormSet(instance=request.user, prefix=CERTIFICATION_FORMS_PREFIX)
    certification_forms_helper = CertificationFormSetHelper()
    skill_forms = SkillFormSet(instance=request.user, prefix=SKILL_FORMS_PREFIX)
    skill_forms_helper = SkillFormSetHelper()
    training_experience_forms = TrainingExperienceFormSet(instance=request.user,
                                                          prefix=TRAINING_EXPERIENCE_FORMS_PREFIX)
    training_experience_forms_helper = TrainingExperienceFormSetHelper()
    return render(request, 'employees/profile.html',
                  {'form': form, 'education_forms': education_forms, 'education_forms_helper': education_forms_helper,
                   'work_experience_forms': work_experience_forms,
                   'work_experience_forms_helper': work_experience_forms_helper,
                   'project_forms': project_forms, 'project_forms_helper': project_forms_helper,
                   'certification_forms': certification_forms, 'certification_forms_helper': certification_forms_helper,
                   'skill_forms': skill_forms, 'skill_forms_helper': skill_forms_helper,
                   'training_experience_form': training_experience_forms,
                   'training_experience_forms_helper': training_experience_forms_helper,
                   })


def post_profile(CertificationFormSet, EducationFormSet, ProjectFormSet, SkillFormSet, TrainingExperienceFormSet,
                 WorkExperienceFormSet, request):
    resume_instance = None
    if hasattr(request.user, 'resume'):
        resume_instance = request.user.resume
    form = ResumeForm(request.POST or None, instance=resume_instance)
    if form.is_valid():
        resume = form.save(commit=False)
        resume.user = request.user
        form.save()
    education_forms = EducationFormSet(request.POST or None, instance=request.user, prefix=EDUCATION_FORMS_PREFIX)
    if education_forms.is_valid():
        education_forms.save()
    work_experience_forms = WorkExperienceFormSet(request.POST or None, instance=request.user,
                                                  prefix=WORK_EXPERIENCE_FORMS_PREFIX)
    if work_experience_forms.is_valid():
        work_experience_forms.save()
    project_forms = ProjectFormSet(request.POST or None, instance=request.user, prefix=PROJECT_FORMS_PREFIX)
    if project_forms.is_valid():
        project_forms.save()
    certification_forms = CertificationFormSet(request.POST or None, instance=request.user,
                                               prefix=CERTIFICATION_FORMS_PREFIX)
    if certification_forms.is_valid():
        certification_forms.save()
    skill_forms = SkillFormSet(request.POST or None, instance=request.user, prefix=SKILL_FORMS_PREFIX)
    if skill_forms.is_valid():
        skill_forms.save()
    training_experience_forms = TrainingExperienceFormSet(request.POST or None, instance=request.user,
                                                          prefix=TRAINING_EXPERIENCE_FORMS_PREFIX)
    if training_experience_forms.is_valid():
        training_experience_forms.save()
    if 'submit-profile' in request.POST:
        resume = request.user.resume
        resume.is_submitted = True
        resume.save()
        messages.success(request, '提交成功')
    else:
        messages.success(request, '保存成功')
    return redirect('profile')


@login_required
def employee_profile(request):
    if allow_view_employee_profile(request):
        CardFormSet = inlineformset_factory(User, Card, form=CardForm, extra=1)
        ContactFormSet = inlineformset_factory(User, ContactPerson, form=ContactForm, extra=1)
        if request.method == 'POST':
            return post_employee(CardFormSet, ContactFormSet, request)

        elif request.method == 'GET':
            return get_employee(CardFormSet, ContactFormSet, request)
        else:
            return Http404('404')
    else:
        return redirect('profile')


def get_employee(CardFormSet, ContactFormSet, request):
    if request.user.employee.is_submitted:
        user = request.user
        return render(request, 'employees/profile-view.html', {'user': user})
    id_card_form = IdCardForm()
    if hasattr(request.user, 'idcard'):
        id_card_form = IdCardForm(instance=request.user.idcard)
    card_forms = CardFormSet(instance=request.user, prefix=CARD_FORMS_PREFIX)
    card_forms_helper = CardFormSetHelper()
    contact_forms = ContactFormSet(instance=request.user, prefix=CONTACT_FORMS_PREFIX)
    contact_forms_helper = ContactFormSetHelper()
    return render(request, 'employees/profile-employee.html',
                  {
                      'id_card_form': id_card_form,
                      'card_forms': card_forms, 'card_forms_helper': card_forms_helper,
                      'contact_forms': contact_forms, 'contact_forms_helper': contact_forms_helper,
                  })


def post_employee(CardFormSet, ContactFormSet, request):
    id_card_instance = None
    if hasattr(request.user, 'idcard'):
        id_card_instance = request.user.idcard
    id_card_form = IdCardForm(request.POST or None, request.FILES, instance=id_card_instance)
    if id_card_form.is_valid():
        id_card = id_card_form.save(commit=False)
        id_card.user = request.user
        id_card_form.save()
    card_forms = CardFormSet(request.POST or None, instance=request.user, prefix=CARD_FORMS_PREFIX)
    if card_forms.is_valid():
        card_forms.save()
    contact_forms = ContactFormSet(request.POST or None, instance=request.user, prefix=CONTACT_FORMS_PREFIX)
    if contact_forms.is_valid():
        contact_forms.save()
    if 'submit-profile' in request.POST:
        employee = request.user.employee
        employee.is_submitted = True
        employee.save()
        messages.success(request, '提交成功')
    else:
        messages.success(request, '保存成功')
    return redirect('employee_profile')


@login_required
def timesheet(request):
    TimeSheetFormSet = inlineformset_factory(User, TimeSheet, fk_name='user', form=TimeSheetForm, extra=1)

    # 获得该用户UserWorkProject的QuerySet
    self_user_work_project_set = UserWorkProject.objects.filter(user=request.user)

    # 构建空的queryset存放workproject
    self_work_project_set = WorkProject.objects.none()

    # 遍历查询workproject
    for item in self_user_work_project_set:
        # 按照id查询workproject，返回queryset（一条数据）
        result = WorkProject.objects.filter(id=item.work_project_id)

        # 将这一条数据追加到workproject的queryset中
        self_work_project_set = self_work_project_set | result

    if request.method == 'POST':
        time_sheet_forms = TimeSheetFormSet(request.POST, instance=request.user, prefix=TIMESHEET_FORMS_PREFIX)
        TimeSheetFormSets = inlineformset_factory(User, TimeSheet, fk_name='user', form=TimeSheetForm, extra=0)
        temporary_forms = TimeSheetFormSets(instance=request.user, prefix=TIMESHEET_FORMS_PREFIX)

        for form in time_sheet_forms:
            form.fields['work_project'].queryset = self_work_project_set

        if time_sheet_forms.is_valid():
            for form in time_sheet_forms:
                if form.changed_data != []:
                    time_percentage = form.cleaned_data['time_percentage']
                    for temp in temporary_forms:
                        if form.cleaned_data['year'] == temp.initial['year'] and form.cleaned_data['month'] == temp.initial['month']:
                            time_percentage += temp.initial['time_percentage']
                        if time_percentage > 100:
                            out_of_range = True
                            time_sheet_form_helper = TimeSheetFormSetHelper()
                            year = form.base_fields['year'].choices[form.cleaned_data['year'] - 1][1]
                            month = form.base_fields['month'].choices[form.cleaned_data['month']][1]
                            work_project = form.cleaned_data['work_project']
                            return render(request, 'employees/profile-timesheet.html', {'work_project': work_project, 'year': year, 'month': month, 'time_sheet_forms': time_sheet_forms, 'time_sheet_form_helper': time_sheet_form_helper, 'out_of_range': out_of_range,})
                    extra = form.save(commit=False)
                    # commit=False告诉Django先不提交到数据库.
                    extra.create_user = request.user  # 添加额外数据
                    extra.alert_user = request.user
            time_sheet_forms.save()
            messages.success(request, '提交成功')
        else:
            time_sheet_form_helper = TimeSheetFormSetHelper()
            project_error = True
            return render(request, 'employees/profile-timesheet.html', {
                'time_sheet_forms': time_sheet_forms, 'time_sheet_form_helper': time_sheet_form_helper,
                'project_error': project_error})
        return redirect('timesheet')

    elif request.method == 'GET':
        time_sheet_forms = TimeSheetFormSet(prefix=TIMESHEET_FORMS_PREFIX)
        for form in time_sheet_forms:
            form.fields['work_project'].queryset = self_work_project_set
        time_sheet_form_helper = TimeSheetFormSetHelper()
        return render(request, 'employees/profile-timesheet.html', {
                                'time_sheet_forms': time_sheet_forms, 'time_sheet_form_helper': time_sheet_form_helper})


@staff_member_required
def interview_resume(request, pk):
    user = User.objects.get(pk=pk)
    template = 'employees/profile-view.html'
    return render(request, template, {'user': user})


def home(request):
    if allow_view_employee_profile(request):
        return redirect('employee_profile')
    else:
        return redirect('profile')


def allow_view_employee_profile(request):
    """
    是否允许当前用户访问员工信息页面
    :param request:
    :return:
    """
    return hasattr(request.user, 'resume') and request.user.resume.is_submitted and hasattr(request.user, 'employee')


def logout_view(request):
    logout(request)
    return redirect('login')


def changepwd(request):
    if request.method == 'GET':
        form = ChangepwdForm()
        return render(request, 'employees/profile-change-password.html', {'form': form, })
    else:
        form = ChangepwdForm(request.POST)
        if form.is_valid():
            username = request.user.username
            oldpassword = request.POST.get('oldpassword', '')
            user = authenticate(username=username, password=oldpassword)
            if user is not None and user.is_active:
                newpassword = request.POST.get('newpassword1', '')
                user.set_password(newpassword)
                user.save()
                return render(request, 'employees/profile-change-password.html', {'changepwd_success': True})
            else:
                return render(request, 'employees/profile-change-password.html', {'form': form, 'oldpassword_is_wrong': True})
        else:
            return render(request, 'employees/profile-change-password.html', {'form': form, })
