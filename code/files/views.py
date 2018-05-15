from django.shortcuts import redirect, get_object_or_404, render
from django.http import HttpResponse
from django.conf import settings
from django.urls import reverse

import json

from sendfile import sendfile
from .models import UploadedFile

from django import forms

# Create your views here.

def download_file(request, filename):
    file = get_object_or_404(UploadedFile, name=filename)

    # Register download here

    filename = file.file_itself.storage.path(file.file_itself.name)
    return sendfile(request, filename, attachment=True, attachment_filename=file.name)


def upload_file(request):
    if request.method == "POST":
        if len(request.FILES) == 0:
            return HttpResponse(status=400, reason="Bad Request: no files was given for upload")
        files = request.FILES.getlist("upload")

        response_files = []

        for file in files:
            uploaded_file = UploadedFile(file_itself=file, name=file.name)
            try: # Remove old file if it exists
                old_file = UploadedFile.objects.get(name=file.name)
                old_file.delete()
            except UploadedFile.DoesNotExist:
                pass # It's ok, no old file exists
            uploaded_file.save()

            thumb_url = "/static/fileicon.png"
            # TODO: detect if file is an image and make a thumbnail for it

            try:
                base_url = settings.UPLOADED_FILE_BASE_URL
            except AttributeError:
                base_url = settings.MEDIA_URL

            if not base_url.endswith("/"):
                base_url += "/"
            direct_url = base_url + uploaded_file.file_itself.name

            response_files.append({
                "name": uploaded_file.name, 
                "url": reverse("download_file", args=(uploaded_file.name,)),
                "direct_url": direct_url,
                "date": uploaded_file.upload_date.strftime("%Y-%m-%d %H:%M"),
                "thumb_url": thumb_url
                })

        return HttpResponse(json.dumps({"files": response_files}), content_type="application/json")
    else:
        resp = HttpResponse("<h1>405 Method Not Allowed</h1>", status=405)
        resp["Allow"] = "POST"
        return resp


def list_files(request):
    files = UploadedFile.objects.all()
    result = []

    try:
        base_url = settings.UPLOADED_FILE_BASE_URL
    except AttributeError:
        base_url = settings.MEDIA_URL

    if not base_url.endswith("/"):
        base_url += "/"

    for file in files:
        thumb_url = "/static/fileicon.png"
        result.append({
            "name": file.name,
            "url": reverse("download_file", args=(file.name,)),
            "direct_url": base_url + file.file_itself.name,
            "date": file.upload_date.strftime("%Y-%m-%d %H:%M"),
            "thumb_url": thumb_url
            })

    return HttpResponse(json.dumps({"files": result}), content_type="application/json")


def upload_test_view(request):

    return render(request, "widget.html")

