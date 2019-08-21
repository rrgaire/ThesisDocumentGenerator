from django.contrib import admin
from .models import Student,CommonFields, Coordinator, Budget

# from proposal.models import notice

# Register your models here.

admin.site.register(Student)
# admin.site.register(CommonFields)
admin.site.register(Coordinator)
admin.site.register(Budget)

