"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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

from .views import TwitListView, IndexView
from . import views


urlpatterns = [
    url(r'^list/$', TwitListView.as_view(), name='twit-list'),
    url(r'^add/$', views.addTwit, name='twit-add'),
    url(r'^$', IndexView.as_view(), name='twit-home'),
    url(r'^logout/$', views.logOut, name='twit-logout'),
]
