# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.urls import path, re_path, include

from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', login_required(TemplateView.as_view(template_name='chat.html')), name='chat'),
]

