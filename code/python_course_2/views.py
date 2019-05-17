from django.shortcuts import render
from django.urls import reverse
from django.http import Http404, HttpResponseRedirect
from django.core.paginator import Paginator
from .utils import get_course_and_prepare_context, visit_timetable, visit_link_posts
from .utils import build_events_and_messages_for_course, build_calendar_from_events
from .utils import set_timezone_to_request, readable_name_for_course
from .timezones import translate_tz_name, make_readable_utc_offset, build_countries_and_timezones_list
from .timezones import find_country_for_timezone
from .models import Course, LinkPost, ReadingItem, Document


def lessons_view(request, course_id=None):
    course, context = get_course_and_prepare_context(request, course_id, "lessons")
    if not course:
        return render(request, "no_course.html", context)
    order = "-date" if course.active else "date"
    lessons = course.lessons.filter(visible=True).order_by(order)
    out_lessons = []
    for l in lessons:
        out_lessons.append({
            "id": l.id,
            "date": l.date,
            "title": l.title,
            "description": l.description,
            "links": l.links.order_by("index")
        })
    context["lessons"] = out_lessons
    return render(request, "lessons.html", context)


def assignments_view(request, course_id=None):
    course, context = get_course_and_prepare_context(request, course_id, "assignments")
    if not course:
        return render(request, "no_course.html", context)

    assignments = course.assignments.filter(visible=True).order_by("date")
    out_assignments = []
    for a in assignments:
        out_assignments.append({
            "id": a.identifier,
            "date": a.date.strftime("%-d %B").lower(),
            "title": a.title,
            "description": a.description
        })
    context["assignments"] = out_assignments
    return render(request, "assignments.html", context)


def assignment_view(request, assignment_id, course_id=None):
    course, context = get_course_and_prepare_context(request, course_id, "one_assignment")
    if not course:
        return render(request, "no_course.html", context)
    try:
        assignment = course.assignments.filter(visible=True, identifier=assignment_id)[0]
    except IndexError:
        raise Http404
    context["assignment"] = {
        "date": assignment.date.strftime("%-d %B").lower(),
        "title": assignment.title,
        "text": assignment.text,
    }
    return render(request, "one_assignment.html", context)


def timetable_view(request):
    course, context = get_course_and_prepare_context(request, None, "timetable")
    if not course:
        return render(request, "no_course.html", context)
    visit_timetable(request, context["now"])
    context["is_timetable_changes"] = False
    user_tz = context["user_tz"]["tz"]
    server_tz = context["server_tz"]
    events, messages = build_events_and_messages_for_course(course, course.start_date, server_tz)
    calendar = build_calendar_from_events(events, user_tz)
    full_user_tz = translate_tz_name(user_tz.zone)
    user_tz_utc = make_readable_utc_offset(context["now"].astimezone(user_tz))
    context["messages"] = messages
    context["calendar"] = calendar
    context["user_tz_name"] = full_user_tz + " (" + user_tz_utc + ")"
    return render(request, "timetable.html", context)


def change_timezone_view(request):
    course, context = get_course_and_prepare_context(request, None, "change_timezone")
    if request.method == "POST":
        if "cb_tz" in request.POST:
            selected_tz = request.POST["cb_tz"]
            set_timezone_to_request(request, selected_tz)
        return HttpResponseRedirect(reverse("timetable_view"))
    else:
        countries, tzlist = build_countries_and_timezones_list(context["now"])
        context["server_time"] = context["now"].strftime("%H:%M")
        user_tz_name = context["user_tz"]["tz"].zone
        user_country_code = find_country_for_timezone(user_tz_name)
        if not user_country_code:
            user_country_code = "RU"
            user_tz_name = "Asia/Novosibirsk"
        context["countries"] = [{"code": c[0], "name": c[1]} for c in countries]
        context["all_tz"] = [
            {
                "code": code,
                "tz": [
                    {
                        "name": tz[1],
                        "tz": tz[0],
                        "time": tz[2]
                    } for tz in val
                ]
            } for code, val in tzlist.items()
        ]
        context["selected_country_code"] = user_country_code
        context["selected_country_tz"] = [
            {
                "name": tz[1],
                "tz": tz[0],
                "time": tz[2]
            } for tz in tzlist[user_country_code]
        ]
        context["selected_tz"] = user_tz_name
        return render(request, "chahge_timezone.html", context)


def linkpost_view(request, course_id=None):
    course, context = get_course_and_prepare_context(request, course_id, "links")
    visit_link_posts(request, context["now"])
    if "page" in request.GET:
        try:
            page = int(request.GET["page"])
        except ValueError:
            page = 1
    else:
        page = 1
    links = LinkPost.objects.order_by("-datetime")
    pager = Paginator(links, 30)
    if page < 1:
        page = 1
    if page > pager.num_pages:
        page = pager.num_pages
    links_page = pager.get_page(page)
    context["links"] = links_page
    return render(request, "links.html", context)


def reading_view(request, course_id=None):
    course, context = get_course_and_prepare_context(request, course_id, "reading")
    reading_items = ReadingItem.objects.order_by("index")
    context["reading_items"] = reading_items
    return render(request, "reading.html", context)


def contacts_view(request, course_id=None):
    course, context = get_course_and_prepare_context(request, course_id, "contacts")
    return render(request, "contacts.html", context)


def courses_view(request):
    try:
        from python_course.models import Course as OldCourse
    except ImportError:
        OldCourse = None
    course, context = get_course_and_prepare_context(request, None, "courses")
    courses = Course.objects.order_by("-start_date")
    out_courses = [
        {
            "name": readable_name_for_course(c),
            "url": reverse("lessons_view") if c.active else reverse("c_lessons_view", kwargs={"course_id": c.identifier}),
            "active": c.active,
        } for c in courses
    ]
    if OldCourse:
        old_courses = OldCourse.objects.order_by("-start_date")
        out_old_courses = [
            {
                "name": readable_name_for_course(c),
                "url": reverse("o_lessons_view", kwargs={"course_id": c.identifier}),
                "active": False
            } for c in old_courses
        ]
        out_courses.extend(out_old_courses)
    context["courses"] = out_courses
    return render(request, "courses.html", context)


def document_view(request, document_id):
    course, context = get_course_and_prepare_context(request, None, "doc")
    try:
        document = Document.objects.get(identifier=document_id)
    except Document.DoesNotExist:
        raise Http404
    context["document"] = document
    return render(request, "document.html", context)
