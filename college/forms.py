from django import forms

from college.models import AssignSubjectTeacher, Batch, Programme, Year

Semester_Choices = {("", '----'), ('First', 'First'), ('Second', 'Second'), ('Third', 'Third'), ('Fourth', 'Fourth')}


class ExportForm(forms.ModelForm):
    year = forms.ModelChoiceField(queryset=Year.objects.all(), required=False)
    batch = forms.ModelChoiceField(queryset=Batch.objects.all(), required=False)
    programme = forms.ModelChoiceField(queryset=Programme.objects.all(), required=False)
    part = forms.ChoiceField(choices={("", '----'), ('Even', 'Even'), ('Odd', 'Odd')}, required=False)
    semester = forms.ChoiceField(choices=Semester_Choices, required=False)

    class Meta:
        model = AssignSubjectTeacher
        fields = ('year', 'batch', 'programme', 'semester', 'part')


class CloneForm(forms.ModelForm):
    Academic_year_from = forms.ModelChoiceField(queryset=Year.objects.all(), required=True)
    Semester_type = forms.ChoiceField(choices={("", '----'), ('Even', 'Even'), ('Odd', 'Odd')}, required=False)
    programme = forms.ModelChoiceField(queryset=Programme.objects.all(), required=False)
    Academic_year_to = forms.ModelChoiceField(queryset=Year.objects.all(), required=False)

    class Meta:
        model = AssignSubjectTeacher
        fields = ('Academic_year_from', 'Academic_year_to', 'programme', 'Semester_type',)
