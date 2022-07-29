"""
ad_catcher URL Configuration.
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/", include("apps.user.urls")),
    path('api/v1/', include("djoser.urls")),
    path('api/v1/', include("djoser.urls.authtoken")),
] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

