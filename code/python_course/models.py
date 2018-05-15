from django.db import models

# Create your models here.

class Course(models.Model):
    identifier = models.SlugField(max_length=30, primary_key=True)
    start_date = models.DateField()
    finished = models.BooleanField(default=False)
    started = models.BooleanField(default=False)

    def __str__(self):
        return self.start_date.strftime("course from %d.%m.%Y")


def timetable_item_index_default():
    return TimetableItem.objects.count()

class TimetableItem(models.Model):
    DAY_NAME_CHOICES = (
        ("Понедельник", "Понедельник"),
        ("Вторник", "Вторник"),
        ("Среда", "Среда"),
        ("Четверг", "Четверг"),
        ("Пятница", "Пятница"),
        ("Суббота", "Суббота"),
        ("Воскресенье", "Воскресенье")
    )
    course = models.ForeignKey(Course, related_name="timetable")
    index = models.IntegerField(default=timetable_item_index_default)
    day_name = models.CharField(max_length=15, choices=DAY_NAME_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return "{} {}-{}".format(self.day_name, self.start_time.strftime("%H:%M"), self.end_time.strftime("%H:%M"))


class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name="lessons")
    identifier = models.SlugField(max_length=50, primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()

    def __str__(self):
        return "{} ({} {}, {})".format(
            self.identifier,
            self.date.strftime("%d.%m.%y"),
            self.title,
            str(self.course))


class LessonLink(models.Model):
    class Meta:
        ordering = ['index']
    index = models.IntegerField(default=0)
    lesson = models.ForeignKey(Lesson, related_name="links")
    text = models.CharField(max_length=200)
    url = models.URLField(blank=True)

    def __str__(self):
        return "[{}] {} <{}>".format(self.index, self.text, self.url)


class Document(models.Model):
    identifier = models.SlugField(max_length=50, primary_key=True)
    title = models.CharField(max_length=200)
    date = models.DateField(null=True, blank=True)
    text = models.TextField()

    def __str__(self):
        return "{} ({})".format(self.identifier, self.title)


class Assignment(models.Model):
    course = models.ForeignKey(Course, related_name="assignments")
    identifier = models.SlugField(max_length=50, primary_key=True)
    date = models.DateField()
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    text = models.TextField()

    def __str__(self):
        return "{} ({} {}, {})".format(self.identifier, self.date.strftime("%d.%m.%y"), self.title, str(self.course))


def reading_item_index_default():
    return len(ReadingItem.objects.all())

class ReadingItem(models.Model):
    index = models.IntegerField(default=reading_item_index_default)
    title = models.CharField(max_length=200)
    description = models.TextField()
    url = models.URLField()

    def __str__(self):
        return "[{}] {}".format(self.index, self.title)
