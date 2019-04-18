from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Button, Div
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm, Textarea
from employees.constants import *
from django import forms
from employees.models import Resume, Education, WorkExperience, Project, Certification, Skill, TrainingExperience, \
    IdCard, Card, ContactPerson, TimeSheet



class LoginForm(AuthenticationForm):
    def __init__(self, request, *args, **kwargs):
        super(LoginForm, self).__init__(request, *args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = 'login'
        self.helper.field_template = 'bootstrap4/layout/inline_field.html'
        self.helper.layout = Layout(
            'username',
            'password',
            Submit('submit', 'Submit', css_class='btn-block')
        )


class ResumeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ResumeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Div('gender', css_class='col-md-2'),
                Div('native_place', css_class='col-md-2'),
                Div('nationality', css_class='col-md-2'),
                Div('birth_date', css_class='col-md-2'),
                Div('height', css_class='col-md-2'),
                Div('weight', css_class='col-md-2'),
                css_class='row'
            ),
            Div(
                Div('telephone', css_class='col-md-3'),
                Div('email', css_class='col-md-3'),
                Div('qq', css_class='col-md-3'),
                Div('wechat', css_class='col-md-3'),
                css_class='row'
            ),
            Div(
                Div('english_level', css_class='col-md-4'),
                Div('english_score', css_class='col-md-4'),
                Div('marital_status', css_class='col-md-4'),
                css_class='row'
            ),
            Div(
                Div('target_position', css_class='col-md-4'),
                Div('expect_salary', css_class='col-md-4'),
                Div('expect_salary_intern', css_class='col-md-4'),
                css_class='row'
            ),
            Div(
                Div('introduction', css_class='col-md-12'),
                css_class='row'
            )
        )

    class Meta:
        model = Resume
        fields = ['gender', 'native_place', 'nationality', 'birth_date', 'marital_status',
                  'target_position', 'expect_salary', 'expect_salary_intern',
                  'telephone', 'email', 'qq', 'wechat',
                  'english_level', 'english_score',
                  'height', 'weight',
                  'introduction']
        widgets = {
            'introduction': Textarea(attrs={'rows': 3})
        }


class EducationFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(EducationFormSetHelper, self).__init__(*args, **kwargs)
        self.form_tag = False

        self.layout = Layout(
            Div(
                Div('school', css_class='col-md-8'),
                Div('major', css_class='col-md-4'),
                css_class='row'
            ),
            Div(
                Div('education', css_class='col-md-3'),
                Div('education_type', css_class='col-md-3'),
                Div('start_date', css_class='col-md-3'),
                Div('end_date', css_class='col-md-3'),
                css_class='row'
            ),
            Button('button', '删除', css_class='btn btn-danger btn-block btn-delete',),
            Div(
                Div('DELETE'),
                css_class='row',
                hidden="true"
            )
        )
        self.layout.extend(['user', 'id'])
        self.all().wrap_together(Div, css_class=EDUCATION_FORMS_PREFIX)


class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = ['school', 'major', 'education', 'education_type', 'start_date', 'end_date']


class WorkExperienceFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(WorkExperienceFormSetHelper, self).__init__(*args, **kwargs)
        self.form_tag = False

        self.layout = Layout(
            Div(
                Div('company_name', css_class='col-md-5'),
                Div('position', css_class='col-md-3'),
                Div('start_date', css_class='col-md-2'),
                Div('end_date', css_class='col-md-2'),
                css_class='row'
            ),
            Div(
                Div('resignation_reason', css_class='col-md-12'),
                css_class='row'
            ),
            Div(
                Div('description', css_class='col-md-12'),
                css_class='row'
            ),
            Button('button', '删除', css_class='btn btn-danger btn-block btn-delete'),
            Div(
                Div('DELETE'),
                css_class='row',
                hidden="true"
            )
        )
        self.layout.extend(['user', 'id'])
        self.all().wrap_together(Div, css_class=WORK_EXPERIENCE_FORMS_PREFIX)


class WorkExperienceForm(ModelForm):
    class Meta:
        model = WorkExperience
        exclude = ['user']
        widgets = {
            'description': Textarea(attrs={'rows': 3})
        }


class ProjectFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(ProjectFormSetHelper, self).__init__(*args, **kwargs)
        self.form_tag = False

        self.layout = Layout(
            Div(
                Div('name', css_class='col-md-8'),
                Div('start_date', css_class='col-md-2'),
                Div('end_date', css_class='col-md-2'),
                css_class='row'
            ),
            Div(
                Div('technology', css_class='col-md-12'),
                css_class='row'
            ),
            Div(
                Div('description', css_class='col-md-12'),
                css_class='row'
            ),
            Div(
                Div('responsibility', css_class='col-md-12'),
                css_class='row'
            ),
            Button('button', '删除', css_class='btn btn-danger btn-block btn-delete'),
            Div(
                Div('DELETE'),
                css_class='row',
                hidden='true'
            )
        )
        self.layout.extend(['user', 'id'])
        self.all().wrap_together(Div, css_class=PROJECT_FORMS_PREFIX)


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = ['user']
        widgets = {
            'technology': Textarea(attrs={'rows': 3}),
            'description': Textarea(attrs={'rows': 3}),
            'responsibility': Textarea(attrs={'rows': 3}),
        }


class CertificationFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(CertificationFormSetHelper, self).__init__(*args, **kwargs)
        self.form_tag = False

        self.layout = Layout(
            Div(
                Div('name', css_class='col-md-6'),
                Div('remark', css_class='col-md-6'),
                css_class='row'
            ),
            Button('button', '删除', css_class='btn btn-danger btn-block btn-delete'),
            Div(
                Div('DELETE'),
                css_class='row',
                hidden='true'
            )
        )
        self.layout.extend(['user', 'id'])
        self.all().wrap_together(Div, css_class=CERTIFICATION_FORMS_PREFIX)


class CertificationForm(ModelForm):
    class Meta:
        model = Certification
        exclude = ['user']


class SkillFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(SkillFormSetHelper, self).__init__(*args, **kwargs)
        self.form_tag = False

        self.layout = Layout(
            Div(
                Div('level', css_class='col-md-2'),
                Div('content', css_class='col-md-10'),
                css_class='row'
            ),
            Button('button', '删除', css_class='btn btn-danger btn-block btn-delete'),
            Div(
                Div('DELETE'),
                css_class='row',
                hidden='true'
            )
        )
        self.layout.extend(['user', 'id'])
        self.all().wrap_together(Div, css_class=SKILL_FORMS_PREFIX)


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        exclude = ['user']


class TrainingExperienceFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(TrainingExperienceFormSetHelper, self).__init__(*args, **kwargs)
        self.form_tag = False

        self.layout = Layout(
            Div(
                Div('name', css_class='col-md-4'),
                Div('organization_name', css_class='col-md-4'),
                Div('start_date', css_class='col-md-2'),
                Div('end_date', css_class='col-md-2'),
                css_class='row'
            ),
            Div(
                Div('content', css_class='col-md-12'),
                css_class='row'
            ),
            Button('button', '删除', css_class='btn btn-danger btn-block btn-delete'),
            Div(
                Div('DELETE'),
                css_class='row',
                hidden="true"
            )
        )
        self.layout.extend(['user', 'id'])
        self.all().wrap_together(Div, css_class=TRAINING_EXPERIENCE_FORMS_PREFIX)


class TrainingExperienceForm(ModelForm):
    class Meta:
        model = TrainingExperience
        exclude = ['user']
        widgets = {
            'content': Textarea(attrs={'rows': '3'})
        }


class IdCardForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(IdCardForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Div('id_card_number', css_class='col-md-6'),
                Div('id_card_address', css_class='col-md-6'),
                css_class='row'
            ),
            Div(
                Div('residence_address', css_class='col-md-6'),
                Div('id_card_photo', css_class='col-md-6'),
                css_class='row'
            ),
        )

    class Meta:
        model = IdCard
        exclude = ['user']


class CardFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(CardFormSetHelper, self).__init__(*args, **kwargs)
        self.form_tag = False

        self.layout = Layout(
            Div(
                Div('number', css_class='col-md-6'),
                Div('bank_name', css_class='col-md-6'),
                css_class='row'
            ),
            Div(
                Div('branch_name', css_class='col-md-6'),
                Div('phone', css_class='col-md-6'),
                css_class='row'
            ),
            Div(Div('is_default', css_class='col-md-12'), css_class='row'),
            Div(Div('remark', css_class='col-md-12'), css_class='row'),
            Button('button', '删除', css_class='btn btn-danger btn-block btn-delete'),
            Div(
                Div('DELETE'),
                css_class='row',
                hidden="true"
            )
        )

        self.layout.extend(['user', 'id'])
        self.all().wrap_together(Div, css_class=CARD_FORMS_PREFIX)


class CardForm(ModelForm):
    class Meta:
        model = Card
        exclude = ['user']
        widgets = {
            'remark': Textarea(attrs={'rows': '3'})
        }


class ContactFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(ContactFormSetHelper, self).__init__(*args, **kwargs)
        self.form_tag = False

        self.layout = Layout(
            Div(
                Div('name', css_class='col-md-3'),
                Div('relationship', css_class='col-md-3'),
                Div('organization', css_class='col-md-3'),
                Div('telephone', css_class='col-md-3'),
                css_class='row'
            ),
            Button('button', '删除', css_class='btn btn-danger btn-block btn-delete'),
            Div(
                Div('DELETE'),
                css_class='row',
                hidden="true"
            )
        )

        self.layout.extend(['user', 'id'])
        self.all().wrap_together(Div, css_class=CONTACT_FORMS_PREFIX)


class ContactForm(ModelForm):
    class Meta:
        model = ContactPerson
        exclude = ['user']


class TimeSheetFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(TimeSheetFormSetHelper, self).__init__(*args, **kwargs)
        self.form_tag = False
        self.layout = Layout(
            Div(
                Div('work_project', css_class='col-md-3'),
                Div('year', css_class='col-md-3'),
                Div('month', css_class='col-md-3'),
                Div('time_percentage', css_class='col-md-3'),
                css_class='row'
            ),
            Button('button', '删除', css_class='btn btn-danger btn-block btn-delete'),
        )
        # 将每一个表单加入‘user’、‘id’两个隐藏标签，使得button“添加”表单成功
        self.layout.extend(['user', 'id'])
        self.all().wrap_together(Div, css_class=TIMESHEET_FORMS_PREFIX)


class TimeSheetForm(ModelForm):
    class Meta:
        model = TimeSheet
        exclude = ['create_user', 'create_time', 'alert_user', 'alert_time']


class ChangepwdForm(forms.Form):
    oldpassword = forms.CharField(
        required=True,
        label=u"原密码",
        error_messages={'required': u'请输入原密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u"原密码",
                'rows': 1,
            }
        ),
    )
    newpassword1 = forms.CharField(
        required=True,
        label=u"新密码",
        error_messages={'required': u'请输入新密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u"新密码",
                'rows': 1,
            }
        ),
    )
    newpassword2 = forms.CharField(
        required=True,
        label=u"确认密码",
        error_messages={'required': u'请再次输入新密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u"确认密码",
                'rows': 1,
            }
        ),
    )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"所有项都为必填项")
        elif self.cleaned_data['newpassword1'] != self.cleaned_data['newpassword2']:
            raise forms.ValidationError(u"两次输入的新密码不一样")
        else:
            cleaned_data = super(ChangepwdForm, self).clean()
        return cleaned_data