from django.urls import path
from .views import api_home, SetMetadataFileUpload

urlpatterns = [
    path('', api_home),
    path('api/files-upload', SetMetadataFileUpload.as_view(), name="files_upload"),
]