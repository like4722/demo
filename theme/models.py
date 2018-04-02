# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib import admin
import os
import django.utils.timezone as timezone

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length =50)
    password = models.CharField(max_length=50)
    email = models.EmailField()

    # 用户名＋上传文件名，对应views.upload_file
class UploadInfo(models.Model):
    username = models.CharField(max_length=50)
    filename = models.CharField(max_length=50)
    pathname = models.FileField(upload_to='upload/')
    create_time = models.DateTimeField(default=timezone.now)
    update_time = models.DateTimeField(default=timezone.now)
    remark = models.CharField(max_length=50)
    def __unicode__(self):
        return self.username

    class Meta:
        ordering = ['-create_time']

class CategoryFile(models.Model):
    category = models.CharField(max_length=32)
    def __str__(self):
        return str(self.category)


class BlogsPost(models.Model):
    title = models.CharField(max_length = 150)
    body = models.TextField()
    timestamp = models.DateTimeField()

class BlogsPostAdmin(admin.ModelAdmin):
    list_display = ('title','timestamp')

admin.site.register(BlogsPost,BlogsPostAdmin)

class Meta:
    ordering = ('-timestamp',)

class message(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=15)

class Article(models.Model):
    STATUS_CHOICES = (
        ('d', 'Draft'),
        ('p', 'Published'),
    )

    title = models.CharField('标题', max_length=70)
    body = models.TextField('正文')
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)
    status = models.CharField('文章状态', max_length=1, choices=STATUS_CHOICES)
    abstract = models.CharField('摘要', max_length=54, blank=True, null=True,
                                help_text="可选，如若为空将摘取正文的前54个字符")
    views = models.PositiveIntegerField('浏览量', default=0)
    likes = models.PositiveIntegerField('点赞数', default=0)
    topped = models.BooleanField('置顶', default=False)

    category = models.ForeignKey('Category', verbose_name='分类',
                                 null=True,
                                 on_delete=models.SET_NULL)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-last_modified_time']


class Category(models.Model):
    name = models.CharField('类名', max_length=20)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)

    def __str__(self):
        return self.name

