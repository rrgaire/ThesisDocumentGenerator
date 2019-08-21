"""mscteachers URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, semester_name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), semester_name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from college import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^.*export.*$', views.exportform),
    url(r'^.*dumpteachers.*$', views.exportteachers, name='dumpteachers'),
    url(r'^.*dumpexperts.*$', views.exportexperts, name='dumpexperts'),
    url(r'^.*cloneyear.*$', views.cloneyear, name='dumpexperts'),
    url(r'^.*about.*$', TemplateView.as_view(template_name='admin/about.html'), name='aboutsystem'),
    url(r'^.*docgen/', include(('thesis.urls', 'thesis'))),

    path('', admin.site.urls),
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      url(r'^__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
