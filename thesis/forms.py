from django import forms
from django.forms import modelformset_factory

from college.models import Teacher
from .models import Student, CommonFields


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'rollNumber', 'thesisTitle', 'supervisor']
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control input-md', 'placeholder': 'Name', 'required': 'True'}),
            'rollNumber': forms.TextInput(
                attrs={'class': 'form-control input-md', 'placeholder': 'Roll Number', 'required': 'True'}),
            'thesisTitle': forms.Textarea(
                attrs={'class': 'form-control input-md', 'rows': 3, 'placeholder': 'Thesis Title'}),
            'supervisor': forms.Select(attrs={'class': 'form-control input-md'}),
            # 'examiner': forms.Select(attrs={'class': 'form-control input-md'})

        }


StudentFormset = modelformset_factory(
    Student,
    fields=['name', 'rollNumber', 'thesisTitle', 'supervisor', 'examiner', 'midterm', 'final',
            'internalMarks', 'finalMarks', 'totalMarks', 'examRollNumber'],
    extra=1,
    # form=FormsetStudentForm,
    widgets={
        'name': forms.TextInput(
            attrs={'class': 'form-control input-md', 'placeholder': 'Name'}),
        'rollNumber': forms.TextInput(
            attrs={'class': 'form-control input-md', 'placeholder': 'Roll Number'}),
        'examRollNumber': forms.TextInput(
            attrs={'class': 'form-control input-md', 'placeholder': 'Exam Roll Number'}),
        'thesisTitle': forms.Textarea(
            attrs={'class': 'form-control input-md', 'rows': 1, 'placeholder': 'Thesis Title'}),
        'supervisor': forms.Select(attrs={'class': 'form-control input-md'}),
        'examiner': forms.Select(attrs={'class': 'form-control input-md'}),
        'internalMarks': forms.TextInput(
            attrs={'class': 'form-control input-md', 'placeholder': 'internal'}),
        'finalMarks': forms.TextInput(
            attrs={'class': 'form-control input-md', 'placeholder': 'final'}),
        'totalMarks': forms.TextInput(
            attrs={'class': 'form-control input-md', 'placeholder': 'total', 'readonly': 'readonly'}),

    })
#
# ExaminerForm = modelformset_factory(
#     Examiner,
#     fields=['name', 'companyName', 'companyAddress', 'remove'],
#     extra=1,
#     # form=FormsetStudentForm,
#     widgets={
#         'name': forms.TextInput(
#             attrs={'class': 'form-control input-md', 'placeholder': 'Name'}),
#         'companyName': forms.TextInput(
#             attrs={'class': 'form-control input-md', 'placeholder': 'Company Name'}),
#         'companyAddress': forms.TextInput(
#             attrs={'class': 'form-control input-md', 'placeholder': 'Address'}),
#     })

# AdministratorForm = modelformset_factory(
#
#     Admin,
#     fields=['coordinatorName', 'programName'],
#     extra=1,
#     min_num=1,
#     max_num=1,
#     widgets={
#         'coordinatorName': forms.TextInput(
#             attrs={'class': 'form-control input-md', 'placeholder': 'Coordinator Name'}),
#         'programName': forms.TextInput(
#             attrs={'class': 'form-control input-md', 'placeholder': 'Program Name'}),
#     })
#
# BudgetFormset = modelformset_factory(
#     Budget,
#     fields=['externalExaminer', 'supervisor', 'staff', 'peon', 'tax'],
#     extra=1,
#     min_num=1,
#     max_num=1,
#     widgets={
#         'externalExaminer': forms.TextInput(
#             attrs={'class': 'form-control input-md', 'placeholder': 'Amount', 'type': 'number'}),
#         'supervisor': forms.TextInput(
#             attrs={'class': 'form-control input-md', 'placeholder': 'Amount', 'type': 'number'}),
#         'staff': forms.TextInput(
#             attrs={'class': 'form-control input-md', 'placeholder': 'Amount', 'type': 'number'}),
#         'peon': forms.TextInput(
#             attrs={'class': 'form-control input-md', 'placeholder': 'Amount', 'type': 'number'}),
#         'tax': forms.TextInput(
#             attrs={'class': 'form-control input-md', 'placeholder': 'Tax %', 'type': 'number'}),
#     })

# SupervisorForm = modelformset_factory(
#     Supervisor,
#     fields=['name', 'remove'],
#     extra=1,
#     # form=FormsetStudentForm,
#     widgets={
#         'name': forms.TextInput(
#             attrs={'class': 'form-control input-md', 'placeholder': 'Name'}),
#     })


class NoticeForm(forms.ModelForm):
    CurrentDate = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control input-md', 'placeholder': '14th Mangsir, 2075', 'required': 'True'}))
    PresentationTime = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control input-md', 'placeholder': '5 minutes', 'required': 'True'}))
    defenseTime = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control input-md', 'placeholder': '1:45 P.M.', 'required': 'True'}))

    class Meta:
        model = CommonFields
        fields = ['defenseDate', 'studentBatch']
        widgets = {
            'defenseDate': forms.TextInput(
                attrs={'class': 'form-control input-md', 'placeholder': 'DefenseDate'}),
            'studentBatch': forms.TextInput(
                attrs={'class': 'form-control input-md', 'placeholder': '2070 (and 2075 if needed)'})
        }


class NoticeFormExtra(forms.Form):
    submissionDate = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control input-md', 'placeholder': '22nd Mangsir, 2075', 'required': 'False'}))
    submissionTime = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control input-md', 'placeholder': '1 P.M.', 'required': 'False'}))


class MidTermThesisCommittee(forms.Form):
    CurrentDate = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control input-md', 'placeholder': '14th Mangsir, 2075', 'required': 'True'}))

    Chairman = forms.ModelChoiceField(queryset=Teacher.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control input-md'}))
    Member = forms.ModelChoiceField(queryset=Teacher.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control input-md'}))
    MemberSecretary = forms.ModelChoiceField(queryset=Teacher.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control input-md'}))


class CurrentDate(forms.Form):
    CurrentDate = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control input-md', 'placeholder': '14th Mangsir, 2075', 'required': 'True'}))

    # Results


ResultFormset = modelformset_factory(
    Student,
    fields=['name', 'rollNumber', 'thesisTitle', 'examRollNumber', 'internalMarks', 'finalMarks'],
    extra=0,
    # form=FormsetStudentForm,
    widgets={
        'name': forms.TextInput(
            attrs={'class': 'form-control input-md', 'placeholder': 'Name', 'readonly': 'readonly'}),
        'rollNumber': forms.TextInput(
            attrs={'class': 'form-control input-md', 'placeholder': 'Roll Number', 'readonly': 'readonly'}),
        'examRollNumber': forms.TextInput(
            attrs={'class': 'form-control input-md', 'placeholder': 'Exam Roll Number'}),
        'thesisTitle': forms.Textarea(
            attrs={'class': 'form-control input-md', 'rows': 1, 'placeholder': 'Thesis Title',
                   'readonly': 'readonly'}),
        'internalMarks': forms.TextInput(
            attrs={'class': 'form-control input-md', 'placeholder': 'internal', 'required': 'True'}),
        'finalMarks': forms.TextInput(
            attrs={'class': 'form-control input-md', 'placeholder': 'final', 'required': 'True'})
    })
