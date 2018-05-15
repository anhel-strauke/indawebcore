from django.contrib import admin
from . import models

# Register your models here.

class TimetableItemsInline(admin.TabularInline):
    model = models.TimetableItem
    extra = 1


@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'identifier', 'started', 'finished')
    inlines = [TimetableItemsInline]


class LessonLinksInline(admin.TabularInline):
    model = models.LessonLink
    extra = 1


@admin.register(models.Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'title', 'date', 'course')
    list_filter = ('course',)
    preserve_filters = True
    ordering = ['date']
    inlines = [LessonLinksInline]


@admin.register(models.Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'title', 'identifier', 'date')
    list_filter = ('course',)
    preserve_filters = True


@admin.register(models.ReadingItem)
class ReadingItemAdmin(admin.ModelAdmin):
    list_display = ('title',)
    ordering = ['index']

@admin.register(models.Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'title', 'date')
    ordering = ['date']
