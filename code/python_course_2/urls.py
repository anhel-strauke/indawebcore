from django.urls import path
from django.contrib import admin

from .views import lessons_view, assignments_view, assignment_view, timetable_view, change_timezone_view
from .views import linkpost_view, reading_view, contacts_view, courses_view, document_view

urlpatterns = [
    path("", lessons_view, name="lessons_view"),
    path("assignments/", assignments_view, name="assignments_view"),
    path("assignments/<slug:assignment_id>/", assignment_view, name="assignment_view"),
    path("timetable/", timetable_view, name="timetable_view"),
    path("timetable/settimezone/", change_timezone_view, name="change_timezone_view"),
    path("posts/", linkpost_view, name="linkpost_view"),
    path("reading/", reading_view, name="reading_view"),
    path("contacts/", contacts_view, name="contacts_view"),
    path("courses/", courses_view, name="courses_view"),
    path("courses/<slug:course_id>/", lessons_view, name="c_lessons_view"),
    path("courses/<slug:course_id>/assignments/", assignments_view, name="c_assignments_view"),
    path("courses/<slug:course_id>/assignments/<slug:assignment_id>/", assignment_view, name="c_assignment_view"),
    path("courses/<slug:course_id>/posts/", linkpost_view, name="c_linkpost_view"),
    path("courses/<slug:course_id>/reading/", reading_view, name="c_reading_view"),
    path("courses/<slug:course_id>/contancts", contacts_view, name="c_contacts_view"),
    path("doc/<slug:document_id>/", document_view, name="document_view"),
]