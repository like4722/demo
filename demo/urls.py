"""demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url,include
from django.contrib import admin
#from theme.views import archive
#admin.autodiscover()
from theme import views
from theme.views import *
from theme import urls
import theme


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'',include(theme.urls)),



    #url(r'^$',archive),
    #url(r'^weblog/', include('zinnia.urls', namespace='zinnia')),
    #url(r'^comments/', include('django_comments.urls')),

    #url(r'^login/$', 'logReg.views.login', name='login'),
    #url(r'^regist/$', 'logReg.views.regist', name='regist'),
    #url(r'^index/$', 'logReg.views.index', name='index'),
    #url(r'^logout/$', 'logReg.views.logout', name='logout'),
]
