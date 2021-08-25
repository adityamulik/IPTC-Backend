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
        set_metadata.save_metadata()        

        # zip_file_path = settings.MEDIA_ROOT + "/images.zip"

        # zip_file = open(zip_file_path, 'rb')

        # response = FileResponse(zip_file, content_type="application/zip")
        # response['Content-Disposition'] = 'attachment; filename=images.zip'

        # Discard files downloaded
        discard_files()

        # return response

        return Response({"status": "OK"})