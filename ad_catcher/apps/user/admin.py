from django.contrib import admin
from .models import ParseJob, PageUrl, Banner


admin.site.register(ParseJob)
admin.site.register(PageUrl)
admin.site.register(Banner)
#admin.site.register(BannerData)