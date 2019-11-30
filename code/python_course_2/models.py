from django.db import models
from datetime import time
from django.utils import timezone


class Course(models.Model):
    identifier = models.SlugField(max_length=30, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    hours = models.FloatField()
    active = models.BooleanField()

    def __str__(self):
        return "{1} - {0}".format(self.start_date.strftime("course from %d.%m.%Y"), self.identifier)

    @staticmethod
    def active_course():
        try:
            return Course.objects.filter(active=True)[0]
        except IndexError:
            try:
                return Course.objects.order_by("-start_date")[0]
            except IndexError:
                return None

    @staticmethod
    def course_by_id_or_active(course_id):
        if course_id is None:
            return Course.active_course()
        else:
            try:
                return Course.objects.get(identifier=course_id)
            except Course.DoesNotExist:
                return None


class TimetableItem(models.Model):
    class Meta:
        ordering = ["weekday"]
    DAY_NAME_CHOICES = (
        (0, "Понедельник"),
        (1, "Вторник"),
        (2, "Среда"),
        (3, "Четверг"),
        (4, "Пятница"),
        (5, "Суббота"),
        (6, "Воскресенье")
    )
    course = models.ForeignKey(Course, related_name="timetable", on_delete=models.CASCADE)
    weekday = models.IntegerField(choices=DAY_NAME_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return "{} {}-{}".format(self.DAY_NAME_CHOICES[self.weekday][1],
                                 self.start_time.strftime("%H:%M"), self.end_time.strftime("%H:%M"))


class TimetableAlteration(models.Model):
    course = models.ForeignKey(Course, related_name="timetable_alterations", on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
    date = models.DateField()
    start_time = models.TimeField(default=time(hour=0, minute=0))
    end_time = models.TimeField(default=time(hour=0, minute=0))
    cancelled = models.BooleanField(default=False)
    message = models.TextField(blank=True)

    def __str__(self):
        if self.cancelled:
            text = "{} cancelled".format(self.date.strftime("%d.%m.%y"))
        else:
            text = "{} added ({}-{})".format(self.date.strftime("%d.%m.%y"),
                                             self.start_time.strftime("%H:%M"),
                                             self.end_time.strftime("%H:%M"))
        if len(self.message) > 0:
            msg = " ({})".format(self.message)
        else:
            msg = ""
        return "{}{}".format(text, msg)


class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)
    visible = models.BooleanField(default=True)
    date = models.DateField()
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return "{}: {} ({})".format(self.date.strftime("%d.%m.%y"),
                                    self.title,
                                    self.course.identifier)


class LessonLink(models.Model):
    class Meta:
        ordering = ['index']
    index = models.IntegerField(default=0)
    lesson = models.ForeignKey(Lesson, related_name="links", on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    url = models.URLField(blank=True)

    def __str__(self):
        return "[{}] {} <{}>".format(self.index, self.text, self.url)

    def is_new_window(self):
        need_same_window = (self.url.startswith("https://anhel.in/python/") or
                            self.url.startswith("https://www.anhel.in/python/") or
                            self.url.startswith("/"))
        if need_same_window:
            return False
        return True


class Assignment(models.Model):
    course = models.ForeignKey(Course, related_name="assignments", on_delete=models.CASCADE)
    identifier = models.SlugField(max_length=50)
    visible = models.BooleanField(default=True)
    date = models.DateField(auto_now=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    text = models.TextField()

    def __str__(self):
        return "{} ({} {}, {})".format(self.identifier, self.date.strftime("%d.%m.%y"), self.title, str(self.course))


class LinkPost(models.Model):
    datetime = models.DateTimeField()
    title = models.CharField(max_length=200)
    url = models.URLField()
    description = models.TextField(blank=True)

    def __str__(self):
        return "{} {} <{}>".format(self.datetime.strftime("%d.%m.%y %H:%M"), self.title, self.url)


def reading_item_index_default():
    return len(ReadingItem.objects.all())


class ReadingItem(models.Model):
    class Meta:
        ordering = ['index']
    index = models.IntegerField(default=reading_item_index_default)
    title = models.CharField(max_length=200)
    description = models.TextField()
    url = models.URLField()

    def __str__(self):
        return "[{}] {}".format(self.index, self.title)


class Document(models.Model):
    identifier = models.SlugField(max_length=50, unique=True)
    title = models.CharField(max_length=200)
    date = models.DateField(null=True, blank=True)
    text = models.TextField()

    def __str__(self):
        return "{} ({})".format(self.identifier, self.title)
