from django.conf.urls import url,include
from django.contrib import admin
import views
admin.autodiscover()

urlpatterns = [
   #url(r'^index/$',views.index),
   # url(r'^login/$',views.login),
    #url(r'^regist/$',views.regist),
    url(r'^upload/$',views.upload_file),
    url(r'^showall/$',views.showall),
    url(r'^download/$',views.download_file)


]