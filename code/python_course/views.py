from django.shortcuts import render
from . import models
from django.http import Http404


def get_course(course_identifier):
    if course_identifier is not None:
        try:
            return models.Course.objects.get(identifier=course_identifier)
        except models.Course.DoesNotExist:
            raise Http404
    else:
        raise Http404


def lessons(request, course_id=None):
    timetable = []
    course = get_course(course_id)
    if course is not None:
        lessons = course.lessons.order_by("date")
        print(course.start_date)
        return render(request, "old_python/lessons.html", context={"course_id": course_id, "course": course, "nav": "lessons", "lessons": lessons, "timetable": timetable})
    else:
        return render(request, "old_python/error_no_course.html", context={"course_id": course_id, "nav": "lessons"})


def assignments(request, course_id=None):
    timetable = []
    course = get_course(course_id)
    if course is not None:
        assignments = course.assignments.order_by("date")
        return render(request, "old_python/assignments.html", context={"course_id": course_id, "course": course, "nav": "assignments", "assignments": assignments, "timetable": timetable})
    else:
        return render(request, "old_python/error_no_course.html", context={"course_id": course_id, "nav": "assignments"})


def one_assignment(request, assignment_identifier, course_id=None):
    timetable = []
    course = get_course(course_id)
    if course is not None:
        try:
            assignment = course.assignments.get(identifier=assignment_identifier)
            if not course.finished:
                timetable = course.timetable.order_by("index")
            return render(request, "old_python/view_assignment.html", context={"course_id": course_id, "course": course, "assignment": assignment, "timetable": timetable})
        except models.Assignment.DoesNotExist:
            raise Http404
    else:
        return render(request, "old_python/error_no_course.html", {"course_id": course_id})


def document(request, doc_identifier, course_id=None):
    timetable = []
    course = get_course(course_id)
    if course is not None:
        if not course.finished:
            timetable = course.timetable.order_by("index")
    try:
        doc = models.Document.objects.get(identifier=doc_identifier)
        return render(request, "old_python/view_document.html", context={"doc": doc, "timetable": timetable})
    except models.Document.DoesNotExist:
        raise Http404    


def reading(request, course_id=None):
    timetable = []
    course = get_course(course_id)
    if course is not None:
        if not course.finished:
            timetable = course.timetable.order_by("index")

    reading_items = models.ReadingItem.objects.order_by("index")
    return render(request, "old_python/reading.html", context={"course_id": course_id, "course": course, "nav": "reading", "reading_items": reading_items, "timetable": timetable})
