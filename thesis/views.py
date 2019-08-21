
import pandas as pd

from django.shortcuts import render, redirect

from . import utils
import os
from thesis.models import Student, CommonFields, Budget, Coordinator
from .forms import NoticeForm, MidTermThesisCommittee, StudentFormset, \
    NoticeFormExtra, CurrentDate, ResultFormset
from django.views.generic import TemplateView


# Create your views here.


def index(request):
    return render(request, 'thesis/home.html')


def invalid(request):
    return render(request, 'thesis/invalid.html')


def proposal_entries(request):
    return render(request, 'thesis/proposal_entries.html')


def midterm_entries(request):
    return render(request, 'thesis/midterm_entries.html')


def final_entries(request):
    return render(request, 'thesis/final_entries.html')


def students(request):
    if request.method == 'POST':
        formset = StudentFormset(request.POST)
        print(formset.errors)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for i in instances:
                if i.midterm is False:
                    i.examiner = None
                    i.final = False
                if not i.internalMarks and not i.finalMarks:
                    i.totalMarks = None

                if i.final is False:
                    i.internalMarks = None
                    i.finalMarks = None
                    i.totalMarks = None
                else:
                    if i.internalMarks and i.finalMarks:
                        i.totalMarks = i.internalMarks + i.finalMarks
                    else:
                        i.totalMarks = None


                i.save()
        return redirect('thesis:students')
    else:
        formset = StudentFormset(queryset=Student.objects.all())
        return render(request, 'thesis/students.html', {'formset': formset})



def proposalNotice(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        formExtra = NoticeFormExtra(request.POST)
        if form.is_valid() and formExtra.is_valid():
            admins = Coordinator.objects.all().get()
            form.save()
            Common = CommonFields.objects.all()
            if len(Common) > 1:
                Common[0].delete()
            context = form.cleaned_data
            contextFormExtra = formExtra.cleaned_data
            defenseDate = str(Common[0].defenseDate)
            studentBatch = str(Common[0].studentBatch)
            context['programName'] = str(admins.programName)
            context['coordinatorName'] = str(admins.coordinatorName)
            context['batch'] = studentBatch
            context['defensedate'] = defenseDate
            context['submissionTime'] = contextFormExtra['submissionTime']
            context['submissionDate'] = contextFormExtra['submissionDate']
            src_add = os.path.join(
                os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Templates'), 'Proposal'),
                'ProposalNotice.docx')
            utils.render_to_word(src_add, os.path.join(
                os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Documents'), 'Proposal'),
                'ProposalNotice.docx'), context)
            return redirect('thesis:index')
        else:
            return redirect('thesis:invalid')

    else:
        form = NoticeForm()
        formExtra = NoticeFormExtra()
        return render(request, 'thesis/proposalAndFinalNotice.html', {'form': form, 'formExtra': formExtra})


def midTermNotice(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        print(form.errors)
        if form.is_valid():
            admins = Coordinator.objects.all().get()
            form.save()
            Common = CommonFields.objects.all()
            if len(Common) > 1:
                Common[0].delete()
            context = form.cleaned_data
            context['programName'] = str(admins.programName)
            context['coordinatorName'] = str(admins.coordinatorName)
            src_add = os.path.join(
                os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Templates'), 'Midterm'),
                'MidtermNotice.docx')
            utils.render_to_word(src_add, os.path.join(
                os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Documents'), 'Midterm'),
                'midtermNotice.docx'), context)
            return redirect('thesis:index')

    else:
        form = NoticeForm()
        context = {'form': form}
        return render(request, 'thesis/midTermNotice.html', context)


def finalNotice(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        formExtra = NoticeFormExtra(request.POST)
        if form.is_valid() and formExtra.is_valid():
            admins = Coordinator.objects.all().get()
            form.save()
            Common = CommonFields.objects.all()
            if len(Common) > 1:
                Common[0].delete()
            context = form.cleaned_data
            contextFormExtra = formExtra.cleaned_data
            context['submissionTime'] = contextFormExtra['submissionTime']
            context['submissionDate'] = contextFormExtra['submissionDate']
            context['programName'] = str(admins.programName)
            context['coordinatorName'] = str(admins.coordinatorName)
            print (context)
            src_add = os.path.join(
                os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Templates'), 'Final'),
                'FinalNotice.docx')
            utils.render_to_word(src_add, os.path.join(
                os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Documents'), 'Final'),
                'finalNotice.docx'), context)
            return redirect('thesis:index')

    else:
        form = NoticeForm()
        formExtra = NoticeFormExtra()
        return render(request, 'thesis/proposalAndFinalNotice.html', {'form': form, 'formExtra': formExtra})


def midtermthesislist(request):
    if request.method == 'POST':
        budgets = Budget.objects.all().get()
        admins = Coordinator.objects.all().get()
        Common = CommonFields.objects.all()
        defenseDate = str(Common[0].defenseDate)
        studentBatch = str(Common[0].studentBatch)
        form = MidTermThesisCommittee(request.POST)
        formset = StudentFormset(request.POST)
        if formset.is_valid() and form.is_valid():
            context1 = form.cleaned_data
            print(context1['Chairman'])
            budgetList = list()  # new
            students = []
            examiners = set()
            supervisor = set()

            stds = formset.save(commit=False)

            for std in stds:
                if std.midterm is True:
                    students.append(std)
                    examiners.add(std.examiner)
                    supervisor.add(std.supervisor)
                std.save()

            noOfStd = len(students)  # new

            budgetList.append({'name': 'Peon', 'post': 'peon', 'number': str(noOfStd),  # new
                               'rate': str(budgets.peon), 'total': str(noOfStd * budgets.peon),
                               'tax': str(float(budgets.tax * noOfStd * budgets.peon * .01)),
                               'net': str(float(noOfStd * budgets.peon - budgets.tax * noOfStd * budgets.peon * .01))})

            budgetList.append({'name': 'Staff', 'post': 'staff', 'number': str(noOfStd),  # new
                               'rate': str(budgets.staff), 'total': str(noOfStd * budgets.staff),
                               'tax': str(float(budgets.tax * noOfStd * budgets.staff * .01)),
                               'net': str(
                                   float(noOfStd * budgets.staff - budgets.tax * noOfStd * budgets.staff * .01))})

            numberOfStudents = str(len(students))

            thesisListElements = dict()
            thesisListElements['CurrentDate'] = context1['CurrentDate']
            thesisListElements['B2'] = studentBatch
            thesisListElements['no'] = numberOfStudents
            thesisListElements['DefenceDate'] = defenseDate
            j = 1
            thesisStdList = list()
            thesisStdList1 = list()

            for std in students:
                evaluation = dict()
                sd = dict()
                sd1 = list()
                sd['id'] = str(j)
                sd['name'] = str(std.name)
                sd['rollNumber'] = str(std.rollNumber)
                sd['thesisTitle'] = str(std.thesisTitle)
                sd['supervisor'] = str(std.supervisor)
                sd['examiner'] = str(std.examiner)
                evaluation.update(sd)
                evaluation['programName'] = str(admins.programName)
                evaluation['date'] = defenseDate
                evaluation['organization'] = str(std.examiner.organization.institute_name)
                thesisStdList.append(sd)

                sd1.append(std.rollNumber)
                sd1.append(std.name)
                sd1.append(std.thesisTitle)
                sd1.append(std.supervisor)
                sd1.append(std.examiner)


                thesisStdList1.append(sd1)


                j = j + 1

                src_add = os.path.join(
                    os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Templates'), 'Midterm'),
                    'evalMid_Committee_Member.docx')
                utils.render_to_word(src_add, os.path.join(os.path.join(os.path.join(
                    os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Documents'), 'Midterm')
                    , 'Evaluation'), 'Committee Member'),
                    (str(std.name) + '\'s_Committe_Member_Evaluation.docx')), evaluation)

                src_add = os.path.join(
                    os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Templates'), 'Midterm'),
                    'evalMid_External_Examiner.docx')
                utils.render_to_word(src_add, os.path.join(os.path.join(os.path.join(
                    os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Documents'), 'Midterm')
                    , 'Evaluation'), 'External Examiner'),
                    (str(std.examiner) + ' External_Evaluation.docx')), evaluation)

                src_add = os.path.join(
                    os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Templates'), 'Midterm'),
                    'evalMid_Supervisor.docx')
                utils.render_to_word(src_add, os.path.join(os.path.join(os.path.join(
                    os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Documents'), 'Midterm')
                    , 'Evaluation'), 'Supervisor'),
                    (str(std.supervisor) + ' Supervisor_Evaluation.docx')), evaluation)

            df1 = pd.DataFrame(thesisStdList1,
                               columns=['Roll NO', 'Name Of Student', 'Thesis Title', 'Supervisor',
                                        ' External Examiner'])
            df1.set_index('Roll NO', inplace=True)
            df1.to_excel(os.path.join(
                os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Documents'), 'Midterm'),
                'candidates-midterm.xlsx'))

            thesisListElements['list'] = thesisStdList
            thesisListElements['programName'] = str(admins.programName)
            thesisListElements['coordinatorName'] = str(admins.coordinatorName)
            thesisListElements['B2'] = studentBatch

            src_add = os.path.join(
                os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Templates'), 'Midterm'),
                'MidtermThesisList.docx')
            utils.make_table(src_add, os.path.join(
                os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Documents'), 'Midterm'),
                'MidtermThesisList.docx'), thesisListElements)

            for suv in supervisor:
                budgetSupervisor = dict()  # new
                i = 0
                for std in students:
                    if str(std.supervisor) == str(suv):
                        i = i + 1

                budgetSupervisor['name'] = str(suv)
                budgetSupervisor['post'] = 'Supervisor'
                budgetSupervisor['number'] = str(i)
                budgetSupervisor['rate'] = str(budgets.supervisor)
                budgetSupervisor['total'] = str(float(budgetSupervisor['rate']) * i)
                budgetSupervisor['tax'] = str(float(float(budgetSupervisor['total']) * budgets.tax * 0.01))
                budgetSupervisor['net'] = str(float(budgetSupervisor['total']) - float(budgetSupervisor['tax']))

                budgetList.append(budgetSupervisor)

            committeeMembers = [str(context1['MemberSecretary']), str(context1['Member']),
                                str(context1['Chairman'])]

            supervisor1 = []

            for i in supervisor:
                supervisor1.append(i)

            k = 0
            for name in committeeMembers:
                if k is 0:
                    post = 'Supervisor Member Secretary'
                elif k is 1:
                    post = 'Supervisor Member'
                else:
                    post = 'Supervisor Chairman'
                k = k + 1
                NOS = noOfStd
                if name in supervisor1:
                    for i in budgetList:
                        if i['name'] == name:
                            NOS = noOfStd - int(i['number'])
                            break

                budgetList.append({'name': name, 'post': post, 'number': str(NOS),  # new
                                   'rate': str(budgets.supervisor), 'total': str(NOS * budgets.supervisor),
                                   'tax': str(float(budgets.tax * NOS * budgets.supervisor * .01)),
                                   'net': str(
                                       float(NOS * budgets.supervisor - budgets.tax * NOS * budgets.supervisor * .01))})

            for examr in examiners:
                context = dict()
                budgetExaminer = dict()  # new
                stdlist = list()
                i = 0
                for std in students:
                    if str(std.examiner) == str(examr):
                        s = dict()
                        s['name'] = str(std.name)
                        s['rollNumber'] = str(std.rollNumber)
                        s['thesisTitle'] = str(std.thesisTitle)
                        stdlist.append(s)
                        i = i + 1
                        s['id'] = str(i)

                budgetExaminer['name'] = str(examr)
                budgetExaminer['post'] = 'External Examiner'
                budgetExaminer['number'] = str(i)
                budgetExaminer['rate'] = str(budgets.externalExaminer)
                budgetExaminer['total'] = str(float(budgetExaminer['rate']) * i)
                budgetExaminer['tax'] = str(float(float(budgetExaminer['total']) * budgets.tax * 0.01))
                budgetExaminer['net'] = str(float(budgetExaminer['total']) - float(budgetExaminer['tax']))

                budgetList.append(budgetExaminer)
                context['programName'] = str(admins.programName)
                context['coordinatorName'] = str(admins.coordinatorName)
                context['ExExaminerName'] = str(examr)
                context['CompanyName'] = str(examr.organization.institute_name)
                context['ComAddress'] = str(examr.organization.address)
                context['CurrentDate'] = context1['CurrentDate']
                context['DefenceDate'] = defenseDate
                context['no'] = numberOfStudents
                context['B2'] = studentBatch

                if len(stdlist) != 0:
                    context['list'] = stdlist
                    src_add = os.path.join(
                        os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Templates'), 'Midterm'),
                        'LetterToExExaminer.docx')
                    utils.make_table(src_add, os.path.join(
                        os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Documents'), 'Midterm'),
                        (str(examr) + ' LetterToExExaminer.docx')), context)

            context2 = dict()
            context2['CurrentDate'] = context1['CurrentDate']
            context2['DefenceDate'] = defenseDate
            context2['no'] = numberOfStudents
            budgetList.reverse()

            for i in range(0, len(budgetList)):
                budgetList[i]['sn'] = str(i + 1)

            context2['list'] = budgetList
            context2['programName'] = str(admins.programName)
            context2['coordinatorName'] = str(admins.coordinatorName)
            context2['taxPercent'] = str(budgets.tax)
            context2['batch'] = studentBatch

            src_add = os.path.join(
                os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Templates'), 'Midterm'),
                'midTermSalaryDistribution.docx')
            utils.make_table(src_add, os.path.join(
                os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Documents'), 'Midterm'),
                'midTermSalaryDistribution.docx'), context2)

            context1['programName'] = str(admins.programName)
            context1['coordinatorName'] = str(admins.coordinatorName)
            context1['DefenceDate'] = defenseDate
            context1['Chairman'] = str(context1['Chairman'])

            context1['Member'] = str(context1['Member'])
            context1['MemberSecretary'] = str(context1['MemberSecretary'])
            context1['Batch'] = studentBatch
            context1['no'] = numberOfStudents

            src_add = os.path.join(
                os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Templates'), 'Midterm'),
                'MidtermCommittee.docx')
            utils.render_to_word(src_add, os.path.join(
                os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Documents'), 'Midterm'),
                'MidtermCommittee.docx'), context1)

            return redirect('thesis:index')

    else:
        form = MidTermThesisCommittee()
        formset = StudentFormset(queryset=Student.objects.filter(midterm=False))
    return render(request, 'thesis/midtermthesislist.html', {'form': form, 'formset': formset})


# Finals

def finalthesislist(request):
    if request.method == 'POST':
        budgets = Budget.objects.all().get()
        admins = Coordinator.objects.all().get()
        Common = CommonFields.objects.all()
        defenseDate = str(Common[0].defenseDate)
        studentBatch = str(Common[0].studentBatch)
        form = MidTermThesisCommittee(request.POST)
        formset = StudentFormset(request.POST)
        if formset.is_valid() and form.is_valid():
            context1 = form.cleaned_data
            budgetList = list()
            students = []
            examiners = set()
            supervisor = set()

            stds = formset.save(commit=False)

            for std in stds:
                if std.final is True:
                    std.midterm = True
                    students.append(std)
                    examiners.add(std.examiner)
                    supervisor.add(std.supervisor)
                std.save()

            noOfStd = len(students)  # new

            budgetList.append({'name': 'Peon', 'post': 'peon', 'number': str(noOfStd),  # new
                               'rate': str(budgets.peon), 'total': str(noOfStd * budgets.peon),
                               'tax': str(float(budgets.tax * noOfStd * budgets.peon * .01)),
                               'net': str(float(noOfStd * budgets.peon - budgets.tax * noOfStd * budgets.peon * .01))})

            budgetList.append({'name': 'Staff', 'post': 'staff', 'number': str(noOfStd),  # new
                               'rate': str(budgets.staff), 'total': str(noOfStd * budgets.staff),
                               'tax': str(float(budgets.tax * noOfStd * budgets.staff * .01)),
                               'net': str(
                                   float(noOfStd * budgets.staff - budgets.tax * noOfStd * budgets.staff * .01))})

            numberOfStudents = str(len(students))

            thesisListElements = dict()
            thesisListElements['CurrentDate'] = context1['CurrentDate']
            thesisListElements['Batch'] = studentBatch
            thesisListElements['no'] = numberOfStudents
            thesisListElements['defenceDate'] = defenseDate
            j = 1
            thesisStdList = list()
            thesisStdList1 = list()

            for std in students:
                evaluation = dict()
                sd = dict()
                sd1 = list()
                sd['id'] = str(j)
                sd['name'] = str(std.name)
                sd['rollNumber'] = str(std.rollNumber)
                sd['thesisTitle'] = str(std.thesisTitle)
                sd['supervisor'] = str(std.supervisor)
                sd['examiner'] = str(std.examiner)

                evaluation.update(sd)
                evaluation['programName'] = str(admins.programName)
                evaluation['date'] = defenseDate
                evaluation['organization'] = str(std.examiner.organization.institute_name)

                thesisStdList.append(sd)

                sd1.append(std.rollNumber)
                sd1.append(std.name)
                sd1.append(std.thesisTitle)
                sd1.append(std.supervisor)
                sd1.append(std.examiner)

                thesisStdList1.append(sd1)

                j = j + 1

                src_add = os.path.join(
                    os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Templates'), 'Final'),
                    'evalfinal_Committee_Member.docx')
                utils.render_to_word(src_add, os.path.join(os.path.join(os.path.join(
                    os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Documents'), 'Final')
                    , 'Evaluation'), 'Committee Member'),
                    (str(std.name) + "'s_Committe_Member_Evaluation.docx")), evaluation)

                src_add = os.path.join(
                    os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Templates'), 'Final'),
                    'evalfinal_External_Examiner.docx')
                utils.render_to_word(src_add, os.path.join(os.path.join(os.path.join(
                    os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Documents'), 'Final')
                    , 'Evaluation'), 'External Examiner'),
                    (str(std.examiner) + ' External_Evaluation.docx')), evaluation)

                src_add = os.path.join(
                    os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Templates'), 'Final'),
                    'evalfinal_Supervisor.docx')
                utils.render_to_word(src_add, os.path.join(os.path.join(os.path.join(
                    os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Documents'), 'Final')
                    , 'Evaluation'), 'Supervisor'),
                    (str(std.supervisor) + ' Supervisor_Evaluation.docx')), evaluation)

            df1 = pd.DataFrame(thesisStdList1,
                               columns=['Roll NO', 'Name Of Student', 'Thesis Title', 'Supervisor',
                                        ' External Examiner'])
            df1.set_index('Roll NO', inplace=True)
            df1.to_excel(os.path.join(
                os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Documents'), 'Final'),
                'candidates-final.xlsx'))

            thesisListElements['list'] = thesisStdList
            thesisListElements['defenseDate'] = defenseDate
            thesisListElements['programName'] = str(admins.programName)
            
            thesisListElements['coordinatorName'] = str(admins.coordinatorName)

            src_add = os.path.join(
                os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Templates'), 'Final'),
                'FinalThesisList.docx')
            utils.make_table(src_add, os.path.join(
                os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Documents'), 'Final'),
                'FinalThesisList.docx'), thesisListElements)

            for suv in supervisor:
                budgetSupervisor = dict()  # new
                i = 0
                for std in students:
                    if str(std.supervisor) == str(suv):
                        i = i + 1

                budgetSupervisor['name'] = str(suv)
                budgetSupervisor['post'] = 'Supervisor'
                budgetSupervisor['number'] = str(i)
                budgetSupervisor['rate'] = str(budgets.supervisor)
                budgetSupervisor['total'] = str(float(budgetSupervisor['rate']) * i)
                budgetSupervisor['tax'] = str(float(float(budgetSupervisor['total']) * budgets.tax * 0.01))
                budgetSupervisor['net'] = str(float(budgetSupervisor['total']) - float(budgetSupervisor['tax']))

                budgetList.append(budgetSupervisor)

            committeeMembers = [str(context1['MemberSecretary']), str(context1['Member']),
                                str(context1['Chairman'])]

            supervisor1 = []

            for i in supervisor:
                supervisor1.append(i)

            k = 0
            for name in committeeMembers:
                if k is 0:
                    post = 'Supervisor Member Secretary'
                elif k is 1:
                    post = 'Supervisor Member'
                else:
                    post = 'Supervisor Chairman'
                k = k + 1
                NOS = noOfStd
                if name in supervisor1:
                    for i in budgetList:
                        if i['name'] == name:
                            NOS = noOfStd - int(i['number'])
                            break

                budgetList.append({'name': name, 'post': post, 'number': str(NOS),  # new
                                   'rate': str(budgets.supervisor), 'total': str(NOS * budgets.supervisor),
                                   'tax': str(float(budgets.tax * NOS * budgets.supervisor * .01)),
                                   'net': str(
                                       float(NOS * budgets.supervisor - budgets.tax * NOS * budgets.supervisor * .01))})

            for examr in examiners:
                context = dict()
                budgetExaminer = dict()
                stdlist = list()
                i = 0
                for std in students:
                    if str(std.examiner) == str(examr):
                        s = dict()
                        s['name'] = str(std.name)
                        s['rollNumber'] = str(std.rollNumber)
                        s['thesisTitle'] = str(std.thesisTitle)
                        stdlist.append(s)
                        i = i + 1
                        s['id'] = str(i)

                budgetExaminer['name'] = str(examr)
                budgetExaminer['post'] = 'External Examiner'
                budgetExaminer['number'] = str(i)
                budgetExaminer['rate'] = str(budgets.externalExaminer)
                budgetExaminer['total'] = str(float(budgetExaminer['rate']) * i)
                budgetExaminer['tax'] = str(float(float(budgetExaminer['total']) * budgets.tax * 0.01))
                budgetExaminer['net'] = str(float(budgetExaminer['total']) - float(budgetExaminer['tax']))

                budgetList.append(budgetExaminer)

                context['programName'] =str(admins.programName)
                context['coordinatorName'] = str(admins.coordinatorName)
                context['ExExaminerName'] = str(examr)
                context['CompanyName'] = str(examr.organization.institute_name)
                context['ComAddress'] = str(examr.organization.address)
                context['CurrentDate'] = context1['CurrentDate']
                context['DefenceDate'] = defenseDate
                context['B2'] = studentBatch
                context['no'] = numberOfStudents

                if len(stdlist) != 0:
                    context['list'] = stdlist
                    src_add = os.path.join(
                        os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Templates'), 'Final'),
                        'LetterToExExaminer.docx')
                    utils.make_table(src_add, os.path.join(
                        os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Documents'), 'Final'),
                        (str(examr) + ' LetterToExExaminer.docx')), context)

            context2 = dict()
            context2['CurrentDate'] = context1['CurrentDate']
            context2['DefenceDate'] = defenseDate
            context2['no'] = numberOfStudents
            budgetList.reverse()

            for i in range(0, len(budgetList)):
                budgetList[i]['sn'] = str(i + 1)

            context2['list'] = budgetList
            context2['programName'] = str(admins.programName)
            context2['coordinatorName'] = str(admins.coordinatorName)
            context2['taxPercent'] = str(budgets.tax)
            context2['batch'] = studentBatch

            src_add = os.path.join(
                os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Templates'), 'Final'),
                'finalSalaryDistribution.docx')
            utils.make_table(src_add, os.path.join(
                os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Documents'), 'Final'),
                'finalSalaryDistribution.docx'), context2)

            context1['programName'] = str(admins.programName)
            context1['coordinatorName'] = str(admins.coordinatorName)
            context1['defenseDate'] = defenseDate
            context1['Chairman'] = str(context1['Chairman'])
            context1['Member'] = str(context1['Member'])
            context1['MemberSecretary'] = str(context1['MemberSecretary'])
            context1['Batch'] = studentBatch
            context1['no'] = numberOfStudents

            src_add = os.path.join(
                os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Templates'), 'Final'),
                'FinalCommittee.docx')
            utils.render_to_word(src_add, os.path.join(
                os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Documents'), 'Final'),
                'FinalCommittee.docx'), context1)
            return redirect('thesis:index')

    else:
        form = MidTermThesisCommittee()
        formset = StudentFormset(queryset=Student.objects.filter(midterm=True).filter(final=False))
    return render(request, 'thesis/finalthesislist.html', {'form': form, 'formset': formset})


# results


def results(request):
    if request.method == 'POST':
        form = CurrentDate(request.POST)
        formset = ResultFormset(request.POST)
        Common = CommonFields.objects.all()
        defenseDate = str(Common[0].defenseDate)
        studentBatch = str(Common[0].studentBatch)
        admins = Coordinator.objects.all().get()
        print(formset.errors)
        if formset.is_valid() and form.is_valid():
            context1 = form.cleaned_data
            instances = formset.save(commit=False)
            students = []
            examiners = set()
            for std in instances:
                std.totalMarks = int(std.internalMarks) + int(std.finalMarks)
                std.midterm = True
                std.final = True
                students.append(std)
                examiners.add(std.examiner)
                std.save()

            numberOfStudents = str(len(students))

            thesisListElements = dict()
            thesisListElements['CurrentDate'] = context1['CurrentDate']
            thesisListElements['Batch'] = studentBatch
            thesisListElements['no'] = numberOfStudents
            thesisListElements['defenseDate'] = defenseDate
            j = 1
            thesisStdList = list()
            for std in students:
                sd = dict()
                sd['id'] = str(j)
                sd['name'] = str(std.name)
                sd['rollNumber'] = str(std.rollNumber)
                sd['thesisTitle'] = str(std.thesisTitle)
                sd['supervisor'] = str(std.supervisor)
                sd['examRollNumber'] = str(std.examRollNumber)
                sd['internalMarks'] = str(std.internalMarks)
                sd['finalMarks'] = str(std.finalMarks)
                sd['totalMarks'] = str(std.totalMarks)
                thesisStdList.append(sd)
                j = j + 1

            thesisListElements['programName'] = str(admins.programName)
            thesisListElements['coordinatorName'] = str(admins.coordinatorName)
            thesisListElements['list'] = thesisStdList

            src_add = os.path.join(
                os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Templates'), 'Final'),
                'FinalThesisResultCover.docx')
            utils.make_table(src_add, os.path.join(
                os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Documents'), 'Final'),
                'FinalThesisResultCover.docx'), thesisListElements)

            src_add = os.path.join(
                os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Templates'), 'Final'),
                'FinalThesisResult.docx')
            utils.make_table(src_add, os.path.join(
                os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Documents'), 'Final'),
                'FinalThesisResult.docx'), thesisListElements)

            return redirect('thesis:index')
    else:
        form = CurrentDate()
        formset = ResultFormset(
            queryset=Student.objects.filter(midterm=True).filter(final=True).filter(totalMarks=None))
        return render(request, 'thesis/results.html', {'formset': formset, 'form': form})
