from django.db import models



from college.models import Teacher, Expert, Programme



class Student(models.Model):
    name = models.CharField(max_length=30)
    rollNumber = models.CharField(max_length=30)
    thesisTitle = models.CharField(max_length=500, null=True, blank=True)
    supervisor = models.ForeignKey(Teacher, on_delete=models.SET_NULL, blank=True, null=True)
    examiner = models.ForeignKey(Expert, on_delete=models.SET_NULL, blank=True, null=True)
    midterm = models.BooleanField(default=False, blank=True)
    final = models.BooleanField(default=False, blank=True)
    internalMarks = models.IntegerField(blank=True, null=True)
    finalMarks = models.IntegerField(blank=True, null=True)
    totalMarks = models.IntegerField(blank=True, null=True)
    examRollNumber = models.CharField(max_length=30, blank=True, null=True)

    def nameroll(self):
        return self.rollNumber + " : " + self.name

    def __str__(self):
        return f'{self.nameroll()}'


class CommonFields(models.Model):
    defenseDate = models.CharField(max_length=100)
    studentBatch = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.defenseDate}'


class Coordinator(models.Model):
    coordinatorName = models.ForeignKey(Teacher, on_delete=models.SET_NULL, blank=True, null=True)
    programName = models.ForeignKey(Programme, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{str(self.coordinatorName)}'

    def save(self, *args, **kwargs):
        if self.__class__.objects.count():
            self.pk = self.__class__.objects.first().pk
        super().save(*args, **kwargs)




class Budget(models.Model):
    externalExaminer = models.FloatField(blank=False, null=False)
    supervisor = models.FloatField(blank=False, null=False)
    staff = models.FloatField(blank=False, null=False)
    peon = models.FloatField(blank=False, null=False)
    tax = models.FloatField(blank=False, null=False)

    def save(self, *args, **kwargs):
        if self.__class__.objects.count():
            self.pk = self.__class__.objects.first().pk
        super().save(*args, **kwargs)
