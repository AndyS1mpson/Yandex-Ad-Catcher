from rest_framework import serializers
from .models import ParseJob, PageUrl, Banner
import dateutil.parser


class ParseJobSerializer(serializers.ModelSerializer):


    pages = serializers.SerializerMethodField(method_name='count_pages')
    class Meta:
        model = ParseJob
        fields = ["id", "url", "status", "start_parse", "end_parse", "pages"]


    def count_pages(self, instance):
        pages = PageUrl.objects.filter(job=instance).count()
        return pages


class PageUrlSerializer(serializers.ModelSerializer):
    banners = serializers.SerializerMethodField(method_name='count_banners')
    class Meta:
        model = PageUrl
        fields = ["id", "full_page", "job", "banners"]
    def count_banners(self, instance):
        banners = Banner.objects.filter(pageurl=instance).count()
        return banners

class BannerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Banner
        fields = ("__all__")
    





