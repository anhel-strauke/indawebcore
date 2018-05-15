from django.contrib import admin
from django.urls import reverse

# Register your models here.
from . import models

def delete_uploaded_files(modeladmin, request, queryset):
    """
    Custom admin action for deleting files. Default bulk delete action doesn't remove files from the storage,
    because it does not call overriden delete() method of UploadedFile model. This action does.
    """
    count = 0
    for obj in queryset:
        obj.delete()
        count += 1
    if count == 1:
        message = "1 file deleted"
    else:
        message = "{} files deleted".format(count)
    modeladmin.message_user(request, message)
delete_uploaded_files.short_description = "Delete selected files completely"

def full_file_url(fileobj):
    return reverse("download_file", args=fileobj.name)
full_file_url.short_description = "URL"


class UploadedFileAdmin(admin.ModelAdmin):
    date_hierarchy = 'upload_date'
    list_display = ('name', 'description', 'upload_date', full_file_url)
    actions = [delete_uploaded_files]
        

admin.site.register(models.UploadedFile, UploadedFileAdmin)

# Disable default delete action. It should be manually enabled for every other model.
admin.site.disable_action('delete_selected')