from django.conf.urls import url, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
	url(r'^$', views.landingpage, name='landingpage'),
	url(r'^dashboard$', views.dashboard, name='dashboard'),
    url(r'^getdata/$', views.get_data)

        ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
