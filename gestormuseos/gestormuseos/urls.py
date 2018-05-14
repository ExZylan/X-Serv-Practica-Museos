"""gestormuseos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import logout, login

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^carga/$', 'museos.views.cargar_museos'),
    url(r'^museos/$', 'museos.views.museoslist'),
    url(r'^museos/(\d+)$', 'museos.views.museo'),
    url(r'^usuario/(\d+)$', 'museos.views.usuario'),
    url(r'^$','museos.views.barra'),
    url(r'^logout', logout),
    url(r'^login', login)
]