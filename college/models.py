import datetime

from django.db import models

# pw - dbms1234


Degree_Choices = {('PhD', 'PhD'), ('Masters', 'Masters'), ('Bachelors', 'Bachelors'), ('Diploma', 'Diploma')}
Semester_Choices = {('First', 'First'), ('Second', 'Second'), ('Third', 'Third'), ('Fourth', 'Fourth')}
Affiliation_Choices = {('Permanent', 'Permanent'), ('Contract', 'Contract'), ('Visiting', 'Visiting')}
Position_Choices = {('Prof Dr.', 'Prof Dr'), ('Dr.', 'Dr'), ('Mr.', 'Mr'), ('Ms.', 'Ms'), ('Mrs.', 'Mrs')}


class Programme(models.Model):
    name = models.CharField(max_length=50, unique=True )

    def __str__(self):
        return self.name


class Year(models.Model):
    name = models.CharField(max_length=40, default=str(int(datetime.date.today().strftime("%Y")) + 57) , unique=True )

    def __str__(self):
        return self.name


class Batch(models.Model):
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
    number_of_students = models.IntegerField(default='20')

    class Meta:
        unique_together = ("year", "programme")

    def __str__(self):
        return self.programme.name + ":" + self.year.name


class Semester(models.Model):
    semester_name = models.CharField(max_length=40, blank=True, null=True, unique=True, choices=Semester_Choices)

    def __str__(self):
        return self.semester_name


class HumanResource(models.Model):
    salutation = models.CharField(max_length=40, choices=Position_Choices, blank=True)
    first_name = models.CharField(max_length=40, )
    middle_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, )
    mobile_phone = models.CharField(max_length=20, blank=True)
    home_phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=30, blank=True)
    upper_degree = models.CharField(max_length=30, choices=Degree_Choices, default='MSc')

    class Meta:
        abstract = True
        unique_together = ("first_name","last_name","mobile_phone", "upper_degree" )

    def full_name(self):
        return str(self.salutation + ' ' + self.first_name + ' ' + self.middle_name + ' ' + self.last_name)

    def __str__(self):
        return self.full_name()


class AffiliatedInstitute(models.Model):
    institute_name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=20)
    address = models.CharField(max_length=50, blank=True)
    office_phone = models.CharField(max_length=20, blank=True)
    office_email = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.institute_name

    class Meta:
        verbose_name = "Organization / Affiliated Institutes"

class Teacher(HumanResource):
    teacher_id = models.CharField(max_length=20, blank=True, null=False)
    # known_subjects = models.ManyToManyField('Subject', null=True)
    aff_type = models.CharField(max_length=30, choices=Affiliation_Choices, default='Permanent')
    affiliated_institute = models.ForeignKey('AffiliatedInstitute', on_delete=models.CASCADE, null=True)
    started_teaching = models.CharField(verbose_name="started teaching in BS",  max_length=4, default=str(int(datetime.date.today().strftime("%Y")) + 57), blank=True)

    def get_known_subjects(self):
        return ",\n".join([p.name for p in self.known_subjects.all()])

    def get_teacher_id(self):
        return str(self.teacher_id)

    def get_teacher_experience_years(self):
        if self.started_teaching:
            return int(str(int(datetime.date.today().strftime("%Y")) + 57)) - int(self.started_teaching)
        else:
            return ""


class Subject(models.Model):
    name = models.CharField(max_length=40, blank=True, null=True, unique=True)
    elective = models.BooleanField(default=False)
    subject_code = models.CharField(max_length=40, blank=True, default=" ")
    # program = models.ForeignKey(Programme, on_delete=models.CASCADE, null=True)
    # semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    # subject_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    credit = models.IntegerField(default="4")
    internal_marks = models.IntegerField(default="40")
    external_marks = models.IntegerField(default="60")

    # def total_marks(self):
    # return self.int_marks + self.ext_marks

    def __str__(self):
        return self.name


class AssignSubjectTeacher(models.Model):
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    # programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
    semester = models.CharField(max_length=40, choices=Semester_Choices)
    subject_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    subject_teacher_teaching_experience_years = models.IntegerField(blank=True, default=0)

    class Meta:
        unique_together = ("year", "batch","subject", "subject_teacher", "semester" )
        verbose_name = "Subject Teacher Assignment"

    def programme(self):
        return self.batch.programme.name

    def getyearpart(self):
        if self.semester == "First":
            return "I/I"
        if self.semester == "Second":
            return "I/II"
        if self.semester == "Third":
            return "II/I"
        if self.semester == "Fourth":
            return "II/II"

    def part(self):
        if self.semester == 'First' or 'Third':
            return 'Odd'
        elif self.semester == 'Second' or 'Fourth':
            return 'Even'

    def __str__(self):
        return self.batch.year.name + " - " + self.batch.programme.name + self.semester + "  :  " + self.subject_teacher.first_name + " , " + self.subject.name


class Topic(models.Model):
    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.name


class Expert(HumanResource):
    organization = models.ForeignKey('AffiliatedInstitute', on_delete=models.CASCADE, null=True)
    topic = models.ManyToManyField(Topic)

    def get_known_topics(self):
        return ",\n".join([p.name for p in self.topic.all()])
