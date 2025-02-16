
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include, re_path
from filebrowser.sites import site
from django.views.i18n import set_language

urlpatterns = [
    path('admin/filebrowser/', site.urls),
    path('grappelli/', include('grappelli.urls')),
    path('',include('frontend.urls',namespace='frontend')),
    path('dashboard/',include('dashboard.urls',namespace='dash')),
    path('tinymce/', include('tinymce.urls')),
    # Language Changer
    path('set-language/', set_language, name='set_language'),

    # rosetta 
    re_path(r'^rosetta/', include('rosetta.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
