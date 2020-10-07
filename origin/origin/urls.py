"""origin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/

    admin:
        URL Path to the Django admin browser interface, need to create a superuser
        to access in terminal
    bonds:
        URL path to the bonds api for GET and POST bonds
    accounts:
        URL path to the login signup and logout pages using default Django templates
    auth:
        URL path to generate an auth token for a registered user

"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('admin/', admin.site.urls),
    path('bonds/', include('bonds.urls')),
    path('accounts/', include('accounts.urls')),
    path('auth/', include('auth.urls'))
]

