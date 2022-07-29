import validators
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Banner, PageUrl, ParseJob
from .serializers import (BannerSerializer, PageUrlSerializer,
                          ParseJobSerializer)


class DefaultPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'

class ParseJobViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = ParseJob.objects.all()
    serializer_class = ParseJobSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    pagination_class = DefaultPagination
    http_method_names = ['get', 'post', 'delete', 'patch']

    def create(self, request, *args, **kwargs):
        if not validators.url(request.data["url"]):
            if validators.domain(request.data["url"]):
                request.data["url"] = f"https://{request.data['url']}"
            else:
                return Response(status=400)
        return super().create(request, *args, **kwargs)

class PageViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = PageUrl.objects.all()
    serializer_class = PageUrlSerializer
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['job']
    http_method_names = ['get', 'post', 'delete', 'patch']

class BannerViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['pageurl']
    http_method_names = ['get', 'post', 'delete', 'patch']

# class BannerDataViewSet(viewsets.ModelViewSet):
#     permission_classes = [permissions.IsAuthenticated]
#     queryset = BannerData.objects.all()
#     serializer_class = BannerDataSerializer
#     pagination_class = DefaultPagination
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     filterset_fields = ['banner']
#     http_method_names = ['get', 'post', 'delete', 'patch']

    # filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # filterset_fields = ['domain', 'project__name', 'status']
    # search_fields = ['domain', 'reg_account__email', 'reg_account__name', 'project__name', 'created', 'last_sync', 'status', 'notes']
    # ordering_fields = ['domain', 'reg_account__email', 'reg_account__name', 'project', 'created', 'last_sync', 'status' ]
