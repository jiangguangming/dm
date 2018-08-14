"""DockerManager URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin

from Auth import urls as authurl
from Auth import views as index_view
from Server import urls as serverurl

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index_view.index, name='index'),
    url(r'^v1/auth/?', include(authurl), name='auth'),
    url(r'^v1/servers/?', include(serverurl), name='server'),
]
