"""aincore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

import files.views
import indaweb.views

urlpatterns = [
    url(r'^$', indaweb.views.index_stub),
    url(r'^control/', admin.site.urls),
    url(r'^files/(.*)$', files.views.download_file, name="download_file"),
    url(r'^act/files/upload', files.views.upload_file, name="act_upload_file"),
    url(r'^act/files/ls', files.views.list_files, name="act_list_files"),
    #url(r'^upload/$', files.views.upload_test_view),
    url(r'^python/', include("python_course.urls"))
]
