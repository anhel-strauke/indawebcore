import calendar
from datetime import date, datetime, timedelta
import pytz
from .timezones import make_tz_shortname_for

from .models import Course, LinkPost, TimetableAlteration
from django.utils.timezone import get_default_timezone

ISO_STRFTIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"
MONTH_NAMES = ("", "январь", "февраль", "март", "апрель", "май", "июнь", "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь")
MONTH_NAMES_ALT = ("", "января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря")

def _month_and_year(dt, do_year=True):
    m = MONTH_NAMES[dt.month]
    if do_year:
        return "{} {}".format(m, dt.year)
    else:
        return m

def readable_name_for_course(course):
    if not course:
        return ""
    try:
        x = course.end_date
    except AttributeError:
        # It's an old course, without end date
        return _month_and_year(course.start_date).capitalize()
    if course.start_date.year == course.end_date.year:
        if course.start_date.month == course.end_date.month:
            return _month_and_year(course.start_date).capitalize()
        else:
            return "{}-{}".format(_month_and_year(course.start_date, do_year=False), _month_and_year(course.end_date)).capitalize()
    else:
        return "{} - {}".format(_month_and_year(course.start_date), _month_and_year(course.end_date)).capitalize()


def datetime_from(a_date, a_time, a_tz):
    """Build datetime object from given date, time and timezone"""
    return a_tz.localize(datetime(a_date.year, a_date.month, a_date.day, a_time.hour, a_time.minute))


def _remove_redundant_weeks(weeks):
    count_if = lambda collection, cond: sum(1 for e in collection if cond(e))
    first_weeks = weeks[:2]
    last_weeks = weeks[-2:]
    if count_if(first_weeks, lambda w: count_if(w, lambda d: d["type"])) == 0:
        return weeks[2:]
    elif count_if(last_weeks, lambda w: count_if(w, lambda d: d["type"])) == 0:
        return weeks[:-2]
    return weeks


def build_events_and_messages_for_course(course, from_date, server_tz):
    """Build list of events for given course, starting from give from_date, server_tz must be a server timezone.
       Returns list of events, each event is a tuple:
       (start_datetime, end_datetime, event_type_str)
    """
    start_date = course.start_date
    end_date = course.end_date
    if start_date > end_date:
        return ([], [])
    res_cal = []
    res_messages = []
    today = date.today()

    timetable_items = {}
    for item in course.timetable.all():
        timetable_items[item.weekday] = (item.start_time, item.end_time)    

    timetable_alts = {}
    for alt in course.timetable_alterations.filter(date__gte=from_date):
        if alt.cancelled:
            timetable_alts[alt.date] = False
        else:
            timetable_alts[alt.date] = (alt.start_time, alt.end_time)
        if alt.date >= today and len(alt.message) > 0:
            res_messages.append(alt.message)

    events = []
    current_day = max(start_date, from_date)
    while current_day <= end_date:
        itm = None
        if current_day.weekday() in timetable_items:
            itm = timetable_items[current_day.weekday()]
        if current_day in timetable_alts:
            alt = timetable_alts[current_day]
            if not alt:
                if itm:
                    time_point = datetime_from(current_day, itm[0], server_tz)
                else:
                    time_point = datetime_from(current_day, time(17, 0), server_tz)
                events.append((time_point, None, "no-lesson"))
            else:
                time_point = datetime_from(current_day, alt[0], server_tz)
                time_end = datetime_from(current_day, alt[1], server_tz)
                events.append((time_point, time_end, "moved-lesson"))
        elif itm:
            time_point = datetime_from(current_day, itm[0], server_tz)
            time_end = datetime_from(current_day, itm[1], server_tz)
            events.append((time_point, time_end, "lesson"))
        current_day += timedelta(days=1)

    return (events, res_messages)


def build_calendar_from_events(events, target_tz):
    """Build calendar for given events list and target (user) timezone.
       events are list of tuples: (datetime_start, datetime_end, event_type_str)
       events list can be creadet by build_events_and_messages_for_course function
       Returns list of months. Each month is a dict:
                    {
                        "month": month_number_from_1_to_12,
                        "month_name": localized_month_name,
                        "year": month_year,
                        "weeks": list of weeks
                    }
                    each week is list of exactly 7 days, each day is a dict:
                    {
                        "day": day_number_or_empty_string_if_day_from_other_month,
                        "type": day_css_class, one of:
                                     "" - usual day,
                                     "lesson" - usual lesson,
                                     "no-lesson" - cancelled lesson,
                                     "moved-lesson" - moved lesson
                        "time_start": time_of_lesson_start_as_string,
                        "time_end": time_of_lesson_end_as_string,
                    }
    """
    
    # Stage 2. Translate events into another time zone and build calendar
    calendar_mgr = calendar.Calendar()

    if not events:
        return ([], res_messages)
    
    targ_start_date = events[0][0].astimezone(target_tz).date()
    targ_end_date = events[-1][0].astimezone(target_tz).date()
    year = targ_start_date.year
    month = targ_start_date.month
    
    res_cal = []

    event_i = 0

    while month <= targ_end_date.month or year < targ_end_date.year:
        res_month = {
            "month": month,
            "month_name": MONTH_NAMES[month],
            "year": year
        }
        weeks = []
        current_week = []
        targ_today = datetime.now(target_tz).date()
        for d in calendar_mgr.itermonthdates(year, month):
            is_today = d == targ_today
            if d.month != month:
                new_day = {
                    "day": "", 
                    "time_start": "", 
                    "time_end": "", 
                    "type": ""
                }
            else:
                new_day = {
                    "day": d.day, 
                    "time_start": "", 
                    "time_end": "", 
                    "type": ""
                }
                if targ_start_date <= d <= targ_end_date and event_i < len(events):
                    if d == events[event_i][0].astimezone(target_tz).date():
                        time_point_start, time_point_end, event_type = events[event_i]
                        event_i += 1
                        new_day["type"] = event_type
                        if event_type != "no-lesson":
                            new_day["time_start"] = time_point_start.astimezone(target_tz).strftime("%H:%M")
                            new_day["time_end"] = time_point_end.astimezone(target_tz).strftime("%H:%M")
                        else:
                            new_day["cancelled"] = True
            if is_today:
                if len(new_day["type"]) > 0:
                    new_day["type"] = "today " + new_day["type"]
                else:
                    new_day["type"] = "today"
            current_week.append(new_day)
            if d.weekday() == 6 and current_week:
                weeks.append(current_week)
                current_week = []
        res_month["weeks"] = _remove_redundant_weeks(weeks)
        res_cal.append(res_month)
        res_month = []
        if month < 12:
            month += 1
        else:
            month = 1
            year += 1
    return res_cal
    

def get_closest_lesson(course, now_in_server_tz, target_tz):
    server_tz = now_in_server_tz.tzinfo
    events, _ = build_events_and_messages_for_course(course, now_in_server_tz.date(), server_tz)
    for e in events:
        time_point_start, time_point_end, event_type = e
        if event_type != "no-lesson":
            return time_point_start.astimezone(target_tz)
    return None


def get_timezone_from_request(request, server_tz):
    session = request.session
    if "tz" in session:
        tz_name = session["tz"]
        try:
            return pytz.timezone(tz_name)
        except pytz.exceptions.UnknownTimeZoneError:
            return server_tz
    else:
        return server_tz


def set_timezone_to_request(request, tz):
    try:
        test = pytz.timezone(tz)
        request.session["tz"] = tz
    except pytz.exceptions.UnknownTimeZoneError:
        request.session["tz"] = get_default_timezone().zone


def is_there_new_link_posts(request):
    if "last_linkpost" in request.session:
        try:
            last_linkpost_date = datetime.strptime(request.session["last_linkpost"], ISO_STRFTIME_FORMAT)
        except ValueError:
            return False
        new_posts = LinkPost.objects.filter(datetime__gt=last_linkpost_date)
        return len(new_posts) > 0
    return False


def is_there_timetable_changes(request, course):
    if not course or not course.active:
        return False
    if "last_timetable" in request.session:
        try:
            last_tt_date = datetime.strptime(request.session["last_timetable"], ISO_STRFTIME_FORMAT)
        except ValueError:
            return False
        new_alts = TimetableAlteration.objects.filter(course=course, date_created__gt=last_tt_date)
        return len(new_alts) > 0
    return False


def visit_link_posts(request, now):
    request.session["last_linkpost"] = now.strftime(ISO_STRFTIME_FORMAT)


def visit_timetable(request, now):
    request.session["last_timetable"] = now.strftime(ISO_STRFTIME_FORMAT)


def make_next_lesson_date(dt):
    month_name = MONTH_NAMES_ALT[dt.month]
    return dt.strftime("%-d {} в %H:%M".format(month_name)).capitalize()


def prepare_context(request, course):
    res = {}
    server_tz = get_default_timezone()
    now = datetime.now(server_tz)
    user_tz = get_timezone_from_request(request, server_tz)
    if course:
        course_name = readable_name_for_course(course)
        course_id = course.identifier
        is_active = course.active
        course_info = {
            "name": course_name,
            "id": course_id,
            "active": is_active
        }
        if is_active:
            next_lesson_dt = get_closest_lesson(course, now, user_tz)
            if next_lesson_dt:
                course_info["next_lesson"] = make_next_lesson_date(next_lesson_dt)
                user_tz_shortname, user_tz_desc = make_tz_shortname_for(next_lesson_dt)
                res["user_tz"] = {
                    "short_name": user_tz_shortname,
                    "short_desc": user_tz_desc
                }
        res["course"] = course_info
    else:
        res["course"] = None
    if "user_tz" not in res:
        user_tz_shortname, user_tz_desc = make_tz_shortname_for(now.astimezone(user_tz))
        res["user_tz"] = {
            "short_name": user_tz_shortname,
            "short_desc": user_tz_desc
        }
    res["user_tz"]["tz"] = user_tz
    res["server_tz"] = server_tz
    res["now"] = now
    res["is_new_linkposts"] = is_there_new_link_posts(request)
    if course:
        res["is_timetable_changes"] = is_there_timetable_changes(request, course)

    return res


def get_course_and_prepare_context(request, course_id, page=""):
    course = Course.course_by_id_or_active(course_id)
    context = prepare_context(request, course)
    if course_id:
        if "course" in context:
            context["course"]["archived"] = True
    context["page"] = page
    if not course:
        if course_id:
            raise Http404
        else:
            return (None, context) 
    return (course, context)