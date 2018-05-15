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
        active_courses = models.Course.objects.filter(started=True, finished=False).order_by("-start_date")
        n = len(active_courses)
        if n > 0:
            return active_courses[n - 1]
        else:
            last_course = models.Course.objects.order_by("-start_date")[:1]
            if len(last_course) > 0:
                return last_course[0]
            return None


def lessons(request, course_name=None):
    timetable = []
    course = get_course(course_name)
    if course is not None:
        lessons = course.lessons.order_by("date")
        if not course.finished:
            timetable = course.timetable.order_by("index")
        return render(request, "lessons.html", context={"nav": "lessons", "lessons": lessons, "timetable": timetable})
    else:
        return render(request, "error_no_course.html", context={"nav": "lessons"})


def assignments(request, course_name=None):
    timetable = []
    course = get_course(course_name)
    if course is not None:
        assignments = course.assignments.order_by("date")
        if not course.finished:
            timetable = course.timetable.order_by("index")
        return render(request, "assignments.html", context={"nav": "assignments", "assignments": assignments, "timetable": timetable})
    else:
        return render(request, "error_no_course.html", context={"nav": "assignments"})


def one_assignment(request, assignment_identifier, course_name=None):
    timetable = []
    course = get_course(course_name)
    if course is not None:
        try:
            assignment = course.assignments.get(identifier=assignment_identifier)
            if not course.finished:
                timetable = course.timetable.order_by("index")
            return render(request, "view_assignment.html", context={"assignment": assignment, "timetable": timetable})
        except models.Assignment.DoesNotExist:
            raise Http404
    else:
        return render(request, "error_no_course.html")


def document(request, doc_identifier, course_name=None):
    timetable = []
    course = get_course(course_name)
    if course is not None:
        if not course.finished:
            timetable = course.timetable.order_by("index")
    try:
        doc = models.Document.objects.get(identifier=doc_identifier)
        return render(request, "view_document.html", context={"doc": doc, "timetable": timetable})
    except models.Document.DoesNotExist:
        raise Http404    


def reading(request):
    timetable = []
    course = get_course(None)
    if course is not None:
        if not course.finished:
            timetable = course.timetable.order_by("index")

    reading_items = models.ReadingItem.objects.order_by("index")
    return render(request, "reading.html", context={"nav": "reading", "reading_items": reading_items, "timetable": timetable})
