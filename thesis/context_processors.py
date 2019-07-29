from thesis.models import Admin
from django.core.exceptions import ObjectDoesNotExist


def base(request):
    try:
        admins = Admin.objects.filter()[:1].get()
        return {'admins': admins}
    except ObjectDoesNotExist:
        admins = {'programName': 'Program Name', 'coordinatorName': 'Click here to add program and coordinator'}
        return {'admins': admins}
