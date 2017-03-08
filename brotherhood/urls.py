from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.views import static


urlpatterns = [
    url(r'', include('bh.urls', namespace='bh')),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns.append(
        url(
            r'^media/(?P<path>.*)$',
            static.serve,
            {'document_root': settings.MEDIA_ROOT}
        )
    )
