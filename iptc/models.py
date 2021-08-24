from django.db import models

class FilesUpload(models.Model):
    id = models.AutoField(primary_key=True)
    images = models.ImageField(upload_to="images", blank=True)
    excel = models.FileField(upload_to="excel", blank=True)
