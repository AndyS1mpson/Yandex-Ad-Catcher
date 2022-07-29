from django.db import models
import os
from auditlog.registry import auditlog


class ParseJob(models.Model):
    url = models.CharField(max_length=1000)
    status = models.CharField(max_length=100)
    start_parse = models.DateTimeField(auto_now_add=True)
    end_parse = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.url

auditlog.register(ParseJob)

class PageUrl(models.Model):
    full_page = models.FileField(null=True, blank=True)
    job = models.ForeignKey(ParseJob, on_delete=models.CASCADE)


class Banner(models.Model):
    file = models.FileField(upload_to='results/%Y/%m/%d/', null=True, blank=True)
    click_url = models.TextField(null=True)
    image_url = models.TextField(null=True)
    pageurl = models.ForeignKey(PageUrl, on_delete=models.CASCADE)
    # created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return os.path.basename(self.file.name)

# class BannerData(models.Model):
#     click_url = models.TextField(null=True)
#     image_url = models.TextField(null=True)
#     banner = models.ForeignKey(Banner, on_delete=models.CASCADE)
