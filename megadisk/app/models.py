from django.db import models
from django.conf import settings


class FilesAndFolders(models.Model):
    name = models.CharField(max_length=250)
    is_folder = models.BooleanField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='amount_files')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='files', blank=True, null=True)
    file = models.FileField(blank=True, null=True)
    uploaded_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    link = models.CharField(max_length=10, blank=True, null=True)
    file_size = models.IntegerField(null=True)
    last_download = models.DateTimeField(blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
