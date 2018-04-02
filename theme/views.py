# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import loader,Context
from django.http import HttpResponse,HttpResponseRedirect
from theme.models import *
from django.views.generic import ListView
import markdown
from django import forms
from django.http import StreamingHttpResponse
import json
import re
import django.utils.timezone as timezone
from django.forms import widgets



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

class UserForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=50)
    password = forms.CharField(label='密码', widget=forms.PasswordInput())
    email = forms.EmailField(label='邮箱')

#文件上传表单
class UploadInfoForm(forms.Form):
    #username = forms.CharField()
    #filename = forms.CharField()
    #pathname = forms.FileField()
    #create_time= forms.CharField()
    category = forms.ChoiceField(label='文件所属分类',choices=CategoryFile.objects.all().values_list('id','category'),widget= widgets.Select)
    remark = forms.CharField(label='描述')

class UserAdmin(admin.ModelAdmin):
    list_display = ('username','password','email')

admin.site.register(User,UserAdmin)

def regist(request):
     if request.method == 'POST':
         userform = UserForm(request.POST)
         if userform.is_valid():
             username = userform.cleaned_data['username']
             password = userform.cleaned_data['password']
             email = userform.cleaned_data['email']

             User.objects.create(username=username,password=password,email=email)
             #User.save()

             return HttpResponse('regist success!!!')
     else:
         userform = UserForm()
     return render_to_response('regist.html',{'userform':userform})

def login(request):
     if request.method == 'POST':
         userform = UserForm(request.POST)
         if userform.is_valid():
             username = userform.cleaned_data['username']
             password = userform.cleaned_data['password']

             user = User.objects.filter(username__exact=username,password__exact=password)

             if user:
                 response = render_to_response('mainpage.html',{'userform':userform})
                 response.set_cookie('cookie_username',username)
                 return response
                 #return render_to_response('template.html',{'userform':userform})
             else:
                 return HttpResponse('用户名或密码错误,请重新登录')

     else:
         userform = UserForm()
     return render_to_response('login.html',{'userform':userform})

#登陆成功
def index(req):
    username = req.COOKIES.get('username','')
    return render_to_response('mainpage.html' ,{'username':username})

#退出
def logout(req):
    response = HttpResponseRedirect("/login/")
    #清理cookie里保存username
    response.delete_cookie('cookie_username')
    return response

def upload_file(request):
    if request.method == "POST":
        # 获取表单信息&写入数据库
        uf = UploadInfoForm(request.POST, request.FILES)
        myFile = request.FILES.get("myfile", None)
        categoryfile = CategoryFile.objects.all()


        if myFile:
            category_id = request.POST.get("category")
            category = categoryfile.get(id=category_id)
            print category
            remark = request.POST.get("remark")
            username = request.COOKIES["cookie_username"]
            user = UploadInfo()
            user.username = username
            user.filename = myFile.name
            user.pathname = "/Users/like/zinnia_demo_env/demo/upload/"+str(category)+"/"+myFile.name
            user.create_time = timezone.now()
            user.update_time = timezone.now()
            user.remark = remark
            user.save()
            f  = request.FILES['myfile']
            path = "/Users/like/zinnia_demo_env/demo/upload/"+str(category)
            print os.path.abspath(path)
            isExists = os.path.exists(path)
            if not isExists:
                os.makedirs(path)
            #destination = open(os.path.join("/Users/like/zinnia_demo_env/demo/upload",str(category),myFile.name),'wb+')
            destination = open(os.path.join(path, myFile.name),
                               'wb+')

            print destination
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()

        #return HttpResponse("upload over!")
        username = request.COOKIES.get('cookie_username', '')
        if (username):
            return render_to_response('upload.html',{'uf':uf})
        else:
            return HttpResponseRedirect("/login/")
    else:
        uf = UploadInfoForm()
    return render_to_response('upload.html',{'uf':uf})

def showall(request):
    uploadinfo = UploadInfo.objects.all()
    username = []
    filename = []
    pathname = []
    create_time = []
    time_different = []
    for info in uploadinfo:
        username.append(info.username)
        filename.append(info.filename)
        pathname.append(info.pathname)
        different = timezone.now()-info.create_time
        time = [re.match(r"\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}",str(info.create_time)).group(0)]
        create_time.append(time)
        time_different.append(different.total_seconds()/3600)
        #create_time.append(info.create_time)
        #username = info.username
        #filename = info.filename
        #pathname = info.pathname
        #break


    username1 = request.COOKIES.get('cookie_username', '')
    if(username1):
        return render(request, 'showall.html', {'username': json.dumps(username), 'filename': json.dumps(filename),
                                                'create_time': json.dumps(create_time),
                                                'time_different': json.dumps(time_different)})

    else:
        return HttpResponseRedirect("/login/")

def show(request):
    uploadinfo = UploadInfo.objects.all()
    username = []
    filename = []
    pathname = []
    create_time = []
    time_different = []
    remark = []
    for info in uploadinfo:
        username.append(info.username)
        filename.append(info.filename)
        pathname.append(info.pathname)
        different = timezone.now() - info.create_time
        time = [re.match(r"\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}", str(info.create_time)).group(0)]
        create_time.append(time)
        time_different.append(different.total_seconds() / 3600)
        remark.append(info.remark)
        # create_time.append(info.create_time)
        # username = info.username
        # filename = info.filename
        # pathname = info.pathname
        # break

    username1 = request.COOKIES.get('cookie_username', '')
    if (username1):
        return render(request, 'show.html', {'username': json.dumps(username), 'filename': json.dumps(filename),
                                                'create_time': json.dumps(create_time),
                                                'time_different': json.dumps(time_different),'remark': json.dumps(remark)})

    else:
        return HttpResponseRedirect("/login/")


def download_file(request,filename):
    uploadinfo = UploadInfo.objects.all()
    path = uploadinfo.get(filename=filename)
    #p ="/Users/like/zinnia_demo_env/demo/upload/others/"+filename
    p1 =path.pathname
    p = str(p1)
    print type(p)
    print p


    def file_iterator(p,chunk_size=512):
        with open(p) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    response = StreamingHttpResponse(file_iterator(p))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(filename.decode('ISO-8859-1'))
    return response

def contact(request):
    username = request.COOKIES.get('cookie_username', '')
    if (username):
        return render_to_response('contact.html', {'username': username})
    else:
        return HttpResponseRedirect("/login/")

def template(request):
    username = request.COOKIES.get('cookie_username', '')
    if(username):
        return render_to_response('template.html', {'username': username})
    else:
        return HttpResponseRedirect("/login/")

    # if request.user.is_authenticated():
    #     username = request.COOKIES.get('cookie_username','')
    #     return render_to_response('template.html',{'username':username})
    # else:
    #     return HttpResponseRedirect("/login/")
def mainpage(request):
    username = request.COOKIES.get('cookie_username', '')
    if (username):
        return render_to_response('mainpage.html', {'username': username})
    else:
        return HttpResponseRedirect("/login/")


def submit(request):
    return render_to_response('submit.html')
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

