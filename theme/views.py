# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import loader,Context
from django.http import HttpResponse
from theme.models import *
from django.views.generic import ListView
import markdown
from django import forms
from django.http import StreamingHttpResponse

# Create your views here.

def archive(request):
    posts = BlogsPost.objects.all()
    t = loader.get_template("archive.html")
    #c = Context({'posts':posts})
    return HttpResponse(t.render({'posts': posts}))
#
# def insert(request):
#     if request.method == "POST":
#         username = request.POST.get("username", None)
#         password = request.POST.get("password", None)
#         message.objects.create(username=username, password=password)
#         message.save()
#     return render_to_response('insert.html')

def list(request):
    people_list = message.objects.all()
    #c = Context({"people_list": people_list})
    return render_to_response("show.html", {"people_list": people_list})

class UserForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=50)
    password = forms.CharField(label='密码', widget=forms.PasswordInput())
    email = forms.EmailField(label='邮箱')

class UploadInfoForm(forms.Form):
    username = forms.CharField()
    #filename = forms.CharField()
    #pathname = forms.FileField()


class UserAdmin(admin.ModelAdmin):
    list_display = ('username','password','email')

admin.site.register(User,UserAdmin)

# def regist(request):
#      if request.method == 'POST':
#          userform = UserForm(request.POST)
#          if userform.is_valid():
#              username = userform.cleaned_data['username']
#              password = userform.cleaned_data['password']
#              email = userform.cleaned_data['email']
#
#              User.objects.create(username=username,password=password,email=email)
#              User.save()
#
#              return HttpResponse('regist success!!!')
#      else:
#          userform = UserForm()
#      return render_to_response('regist.html',{'userform':userform})
#
# def login(request):
#      if request.method == 'POST':
#          userform = UserForm(request.POST)
#          if userform.is_valid():
#              username = userform.cleaned_data['username']
#              password = userform.cleaned_data['password']
#
#              user = User.objects.filter(username__exact=username,password__exact=password)
#
#              if user:
#                  return render_to_response('index.html',{'userform':userform})
#              else:
#                  return HttpResponse('用户名或密码错误,请重新登录')
#
#      else:
#          userform = UserForm()
#      return render_to_response('login.html',{'userform':userform})

def upload_file(request):
    if request.method == "POST":
        # 获取表单信息&写入数据库
        uf = UploadInfoForm(request.POST, request.FILES)
        myFile = request.FILES.get("myfile", None)
        if uf.is_valid():
            username = uf.cleaned_data["username"]
            user = UploadInfo()
            user.username = username
            user.filename = myFile.name
            user.pathname = "/Users/like/zinnia_demo_env/demo/demo/static/"+myFile.name
            user.save()
            f = request.FILES['myfile']
            print f
            destination = open(os.path.join("/Users/like/zinnia_demo_env/demo/demo/static",myFile.name),'wb+')
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()

        return HttpResponse("upload over!")


    else:
        uf = UploadInfoForm()
    return render_to_response('upload.html',{'uf':uf})

def showall(request):
    uploadinfo = UploadInfo.objects.all()
    for info in uploadinfo:
        username = info.username
        filename = info.filename
        pathname = info.pathname
        break
    return render_to_response('showall.html',{'uploadinfo':uploadinfo,'username':username,'filename':filename})

def download_file(request):
    def file_iterator(file_name,chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break


# class IndexView(ListView):
#     """
#     首页视图,继承自ListVIew，用于展示从数据库中获取的文章列表
#     """
#
#     template_name = 'index.html'
#     # template_name属性用于指定使用哪个模板进行渲染
#
#     context_object_name = "article_list"
#     model = Article
#     #context_object_name属性用于给上下文变量取名（在模板中使用该名字）
#
#     def get_queryset(self):
#         print '2'
#         """
#         过滤数据，获取所有已发布文章，并且将内容转成markdown形式
#         """
#         article_list = Article.objects.filter(status='p')
#         # 获取数据库中的所有已发布的文章，即filter(过滤)状态为'p'(已发布)的文章。
#         for article in article_list:
#             article.body = markdown.markdown(article.body, )
#             # 将markdown标记的文本转为html文本
#         return article_list
#
#     def get_context_data(self, **kwargs):
#         print '1'
#             # 增加额外的数据，这里返回一个文章分类，以字典的形式
#         kwargs['category_list'] = Category.objects.all().order_by('name')
#         print '2'
#         return super(IndexView, self).get_context_data(**kwargs)

