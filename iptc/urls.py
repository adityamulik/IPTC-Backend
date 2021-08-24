from django.urls import path
from .views import api_home, FilesUpload

urlpatterns = [
    path('', api_home),
    path('api/files-upload', FilesUpload.as_view(), name="files_upload"),
]