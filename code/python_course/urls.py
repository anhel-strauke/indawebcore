from django.conf.urls import url
from django.contrib import admin
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    url(r'^$', views.lessons, name="lessons_view"),
    url(r'^assignments/$', views.assignments, name="assignments_view"),
    url(r'^assignments/(.+)/$', views.one_assignment, name="assignment_view"),
    url(r'^reading/$', views.reading, name="reading_view"),
    url(r'^doc/(.+)/$', views.document, name="doc_view"),
]