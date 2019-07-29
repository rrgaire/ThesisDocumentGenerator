from django.db import models


# Create your models here.
class Supervisor(models.Model):
    name = models.CharField(max_length=30)
    remove = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'


class Examiner(models.Model):
    name = models.CharField(max_length=50)
    companyName = models.CharField(max_length=100)
    companyAddress = models.CharField(max_length=100)
    remove = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'


class Student(models.Model):
    name = models.CharField(max_length=30)
    rollNumber = models.CharField(max_length=30)
    thesisTitle = models.CharField(max_length=500, null=True, blank=True)
    supervisor = models.ForeignKey(Supervisor, on_delete=models.SET_NULL, blank=True, null=True)
    examiner = models.ForeignKey(Examiner, on_delete=models.SET_NULL, blank=True, null=True)
    midterm = models.BooleanField(default=False, blank=True)
    final = models.BooleanField(default=False, blank=True)
    remove = models.BooleanField(default=False)
    internalMarks = models.IntegerField(blank=True, null=True)
    finalMarks = models.IntegerField(blank=True, null=True)
    totalMarks = models.IntegerField(blank=True, null=True)
    examRollNumber = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return f'{self.name}'


class CommonFields(models.Model):
    defenseDate = models.CharField(max_length=100)
    studentBatch = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.defenseDate}'


class Admin(models.Model):
    coordinatorName = models.CharField(max_length=100)
    programName = models.CharField(max_length=1000)

    def __str__(self):
        return f'{self.coordinatorName}'


class Budget(models.Model):
    externalExaminer = models.FloatField(blank=False, null=False)
    supervisor = models.FloatField(blank=False, null=False)
    staff = models.FloatField(blank=False, null=False)
    peon = models.FloatField(blank=False, null=False)
    tax = models.FloatField(blank=False, null=False)
