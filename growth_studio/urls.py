"""growth_studio URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from homepage.views import index
from blog.views import blog_list, blog_detail
from crawler.views import index as crawler_index, banner as crawler_banner

urlpatterns = [
    url(r'^$', crawler_index),
    url(r'^banner', crawler_banner),
    url(r'^admin/', admin.site.urls),
    url(r'^blog/$', blog_list),
    url(r'^blog/(?P<slug>[^\.]+).html', blog_detail, name='blog_view')
]

urlpatterns += staticfiles_urlpatterns()
