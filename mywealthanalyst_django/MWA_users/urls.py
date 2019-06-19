from django.conf.urls import url, include
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
	url(r'^login/$', views.login_view, name='login'),
    url(r'^register/$', views.register_view, name='register'),
	url(r'^logout/$', views.logout_view, name='logout'),
    path('', include('django.contrib.auth.urls')),  # for password resets
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),


        ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
