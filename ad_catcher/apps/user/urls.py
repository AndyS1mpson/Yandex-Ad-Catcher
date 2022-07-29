from django.urls import path, include
from rest_framework import routers
from . import views



router = routers.DefaultRouter()
router.register(r'parse-job', views.ParseJobViewSet, 'parse-job')
router.register(r'pageurl', views.PageViewSet, 'pageurl')
router.register(r'banner', views.BannerViewSet, 'banner')
# router.register(r'banner-data', views.BannerDataViewSet, 'banner-data')


urlpatterns = [
    path('', include(router.urls)),
]
