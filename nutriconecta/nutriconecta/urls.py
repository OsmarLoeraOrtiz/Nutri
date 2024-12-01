from django.contrib import admin
from django.urls import path, re_path, include
from home.views import *
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from chat.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', Home.as_view(), name = 'home'),
    path('', include('home.urls')),
    path('nutriologo/', include('nutriologo.urls')),
    path('login/', include('login.urls')),
    path('paciente/', include('paciente.urls')),
    path('chat/', include('chat.urls')),
    re_path(r'', include('django_private_chat2.urls', namespace='django_private_chat2')),
    path('users/', UsersListView.as_view(), name='users_list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
