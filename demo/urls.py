
from django.contrib import admin
from django.urls import path , include ,re_path
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , include('core.urls')),
    path('api-auth/', include('rest_framework.urls')),
    re_path(r'^rest-auth/', include('rest_auth.urls')),
    re_path(r'^rest-auth/registration/', include('rest_auth.registration.urls'))

]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
        
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL , document_root= settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL , document_root= settings.STATIC_ROOT)
    