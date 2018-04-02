# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from theme import models

# Register your models here.
class Info(admin.ModelAdmin):
    list_display = ('username', 'filename', 'pathname', 'create_time')


#admin.site.register(models.UploadInfo)
admin.site.register(models.CategoryFile)
admin.site.register(models.UploadInfo,Info)