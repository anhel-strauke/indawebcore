from django.contrib import admin

from .models import Course, TimetableItem, TimetableAlteration, Lesson, LessonLink, Assignment, LinkPost, ReadingItem, Document

# Register your models here.
class TimetableItemsInline(admin.TabularInline):
    model = TimetableItem


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("identifier", "start_date", "end_date", "active")
    inlines = [TimetableItemsInline]
    ordering = ["start_date"]


@admin.register(TimetableAlteration)
class TimetableAlterationAdmin(admin.ModelAdmin):
    list_display = ("date_created", "date", "cancelled", "start_time", "end_time", "course", "message")
    list_filter = ("course",)
    ordering = ["date_created", "date"]
    preserve_filters = True
    date_hierarchy = "date_created"


class LessonLinkInline(admin.TabularInline):
    model = LessonLink
    extra = 1


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("date", "title", "visible", "course")
    list_filter = ("course", "visible")
    preserve_filters = True
    ordering = ["date"]
    date_hierarchy = "date"
    inlines = [LessonLinkInline]


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("date", "identifier", "title", "visible", "course")
    list_filter = ("course", "visible")
    preserve_filters = True
    ordering = ["date"]
    date_hierarchy = "date"


@admin.register(LinkPost)
class LinkPostAdmin(admin.ModelAdmin):
    list_display = ("datetime", "title", "url")
    date_hierarchy = "datetime"
    ordering = ["-datetime"]

@admin.register(ReadingItem)
class ReadingItemAdmin(admin.ModelAdmin):
    list_display = ("title", "url")
    ordering = ["index"]


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("identifier", "title", "date")
    ordering = ["date"]
    date_hierarchy = "date"
