# -*- coding: UTF-8 -*-
import sys
reload(sys)
from django.conf import settings
sys.setdefaultencoding('utf8')

from django.conf.urls import url,include
from django.contrib import admin
import views
admin.autodiscover()

urlpatterns = [
   #url(r'^index/$',views.index),
   # url(r'^login/$',views.login),
    #url(r'^regist/$',views.regist),
    url(r'^$', views.login, name='login'),
    url(r'^login/$',views.login,name = 'login'),
    url(r'^regist/$',views.regist,name = 'regist'),
    url(r'^index/$',views.index,name = 'index'),
    url(r'^logout/$',views.logout,name = 'logout'),
    url(r'^uploadfile/$',views.upload_file),
    url(r'^showall/$',views.showall),
    url(r'^show/$',views.show),
    url(r'^download/filename=(?P<filename>.*)/$',views.download_file),
    url(r'^template/$', views.template),
    url(r'^contact/$', views.contact),
    url(r'^contact/submit.*$', views.submit),
    url(r'^mainpage/$', views.mainpage),
    url(r'^logout/$', views.logout),
    url( r'^static/(?P<path>.*)$', 'django.views.static.serve',{ 'document_root': settings.STATIC_PATH }),


]