from django.urls import path
from .views import api_home, SetMetadataFileUpload, GetMetadataFileUpload, ValidateExcel

urlpatterns = [
    path('', api_home),
    path('api/save-metadata', SetMetadataFileUpload.as_view(), name="set_metadata"),
    path('api/get-metadata', GetMetadataFileUpload.as_view(), name="get_metadata"),
    path('api/validate-excel', ValidateExcel.as_view(), name="validate_excel"),
]