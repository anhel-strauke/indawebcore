from django.conf.urls import url
from django.urls import path
from django.contrib import admin
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    path('<slug:course_id>/', views.lessons, name="o_lessons_view"),
    path('<slug:course_id>/assignments/', views.assignments, name="o_assignments_view"),
    path('<slug:course_id>/assignments/<slug:assignment_identifier>/', views.one_assignment, name="o_assignment_view"),
    path('<slug:course_id>/reading/', views.reading, name="o_reading_view"),
]