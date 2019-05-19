from django.conf.urls import url, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
	url(r'^login/$', views.login_view, name='login'),
    url(r'^register/$', views.register_view, name='register'),
	url(r'^logout/$', views.logout_view, name='logout'),

        ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
