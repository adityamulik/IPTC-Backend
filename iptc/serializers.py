from rest_framework import serializers
from .models import FilesUpload


class FilesUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilesUpload
        fields = '__all__'
