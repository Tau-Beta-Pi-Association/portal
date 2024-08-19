from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('captcha/', include('captcha.urls')),
]
