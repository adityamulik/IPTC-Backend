import zipfile
import os
from io import StringIO
import shutil

from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.conf import settings

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from iptc.iptc_handler import IPTCKeyword, modify_input_for_multiple_files, discard_files
from .serializers import FilesUploadSerializer
from .models import FilesUpload

def api_home(request):
    """
    returns api home page.
    """
    return HttpResponse("<h1>IPTC API Homepage</h1>")


class SetMetadataFileUpload(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        files_upload = FilesUpload.objects.all()
        serializer = FilesUploadSerializer(files_upload, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):

        # Serialize Images and save to media
        images = dict((request.data).lists())['images']

        for i, img_name in enumerate(images):
            modified_data = modify_input_for_multiple_files(i,
                                                            img_name)   
            file_serializer = FilesUploadSerializer(data=modified_data)
            if file_serializer.is_valid():
                file_serializer.save()

        excel_main = {"id": 5, "excel": request.data['excel']}    

        excel_serializer = FilesUploadSerializer(data=excel_main)
        if excel_serializer.is_valid():
            excel_serializer.save()

        # IPTC Function goes here
        excel = settings.MEDIA_ROOT + "/excel/iptc_metadata.csv"

        set_metadata = IPTCKeyword(excel)
        saved = set_metadata.save_metadata()     
        # print(saved)   

        # Zip images and return in response.
        images = settings.MEDIA_ROOT + "/images/"
        shutil.make_archive("images", "zip", images)
        images_zip = open(settings.BASE_DIR + "/images.zip", "rb")

        response = HttpResponse(images_zip, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=images.zip'

        discard_files()

        return response


class GetMetadataFileUpload(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        files_upload = FilesUpload.objects.all()
        serializer = FilesUploadSerializer(files_upload, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Serialize Images and save to media
        images = dict((request.data).lists())['images']

        for i, img_name in enumerate(images):
            modified_data = modify_input_for_multiple_files(i,
                                                            img_name)   
            file_serializer = FilesUploadSerializer(data=modified_data)
            if file_serializer.is_valid():
                file_serializer.save()

        excel_main = {"id": 5, "excel": request.data['excel']}    

        excel_serializer = FilesUploadSerializer(data=excel_main)
        if excel_serializer.is_valid():
            excel_serializer.save()

        # IPTC Function goes here
        excel = settings.MEDIA_ROOT + "/excel/iptc_metadata.csv"

        get_metadata = IPTCKeyword(excel)
        saved = get_metadata.get_metadata()

        discard_files()

        return Response({"Success": 200})


class ValidateExcel(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        files_upload = FilesUpload.objects.all()
        serializer = FilesUploadSerializer(files_upload, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):

        # Serialize Images and save to media
        images = dict((request.data).lists())['images']

        for i, img_name in enumerate(images):
            modified_data = modify_input_for_multiple_files(i,
                                                            img_name)   
            file_serializer = FilesUploadSerializer(data=modified_data)
            if file_serializer.is_valid():
                file_serializer.save()

        excel_main = {"id": 5, "excel": request.data['excel']}    

        excel_serializer = FilesUploadSerializer(data=excel_main)
        if excel_serializer.is_valid():
            excel_serializer.save()

        # IPTC Function goes here
        excel = settings.MEDIA_ROOT + "/excel/iptc_metadata.csv"

        set_metadata = IPTCKeyword(excel)
        response = set_metadata.validate_excel()     

        discard_files()

        return Response(response)