from django.contrib import admin
from .models import Student, Supervisor, Examiner, CommonFields, Admin, Budget

# from proposal.models import notice

# Register your models here.

admin.site.register(Student)
admin.site.register(Supervisor)
admin.site.register(Examiner)
admin.site.register(CommonFields)
admin.site.register(Admin)
admin.site.register(Budget)

