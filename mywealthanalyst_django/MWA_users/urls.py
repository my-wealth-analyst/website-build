from django.conf.urls import url, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
	url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register')

        ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
