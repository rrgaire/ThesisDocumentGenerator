from django.contrib import admin
from django.contrib.admin import AdminSite, ModelAdmin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy
from import_export.admin import ImportExportModelAdmin

from .models import *


# https://docs.djangoproject.com/en/2.0/ref/contrib/admin/#modeladmin-objects
def custom_titled_filter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance

    return Wrapper


class AdminSite(AdminSite):
    site_url = None

    # Text to put at the end of each page's <title>.
    site_title = gettext_lazy('MSc Teachers & Experts Database - IOE, DOECE')

    # Text to put in each page's <h1>.
    site_header = gettext_lazy('MSc Teachers & Experts Database')

    # Text to put at the top of the admin index page.
    index_title = gettext_lazy('Welcome!')


admin.site = AdminSite()
admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)


class ExpertAdmin(ImportExportModelAdmin):
    list_display = (
        'full_name', 'mobile_phone', 'email', 'organization', 'upper_degree', 'get_topics')
    list_filter = ('organization__institute_name', 'upper_degree',)
    search_fields = (
        'first_name', 'last_name', 'middle_name', 'salutation', 'mobile_phone', 'email', 'organization__institute_name',
        'upper_degree', 'topic__name')

    def get_topics(self, obj):
        return ",\n".join([p.name for p in obj.topic.all()])

    get_topics.short_description = "Topics Known"

    pass


class TopicAdmin(ImportExportModelAdmin):
    pass


class TeacherAdmin(ImportExportModelAdmin):
    list_filter = ('affiliated_institute__institute_name', 'upper_degree', 'aff_type')
    list_display = (
        'full_name', 'mobile_phone', 'email', 'affiliated_institute', 'upper_degree', 'aff_type',)
    search_fields = (
        'first_name', 'last_name', 'middle_name', 'salutation', 'mobile_phone', 'email',
        'affiliated_institute__institute_name',
        'upper_degree', 'aff_type')


class SubjectAdmin(ImportExportModelAdmin):
    list_filter = ('elective',)
    list_display = (
        'name', 'internal_marks', 'elective')
    search_fields = ('name',)
    pass


class SubjectTeacherAdmin(ModelAdmin):
    save_as = True
    list_filter = (
        ('year', custom_titled_filter('Academic Year')), ('batch__year__name', custom_titled_filter('Batch Year')),
        ('batch__programme__name', custom_titled_filter('Program Name')), 'semester',
        ('subject_teacher__first_name', custom_titled_filter('Teachers First Name')),
        ('subject__name', custom_titled_filter('Subject Name')))
    list_display = (
        'year', 'batch', 'semester', 'subject_teacher', 'subject')
    search_fields = (
        'year__name', 'batch__year__name', 'batch__programme__name', 'semester', 'subject_teacher__first_name',
        'subject__name')

    pass


class BatchAdmin(ImportExportModelAdmin):
    save_as = True
    pass


admin.site.register(AssignSubjectTeacher, SubjectTeacherAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Expert, ExpertAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Batch, BatchAdmin)
admin.site.register(Programme, ImportExportModelAdmin)
admin.site.register(AffiliatedInstitute, ImportExportModelAdmin)
admin.site.register(Year, ImportExportModelAdmin)
