from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.conf import settings

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from iptc.iptc_handler import IPTCKeyword, modify_input_for_multiple_files
from .serializers import FilesUploadSerializer
from .models import FilesUpload

def api_home(request):
    """
    returns api home page.
    """
    return HttpResponse("<h1>IPTC API Homepage</h1>")


class FilesUpload(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        files_upload = FilesUpload.objects.all()
        serializer = FilesUploadSerializer(files_upload, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):

        # Serialize Images and save to media
        
        images = dict((request.data).lists())['images']
        print(images)

        flag = 1
        arr = []
        for i, img_name in enumerate(images):
            # print(i)
            modified_data = modify_input_for_multiple_files(i,
                                                            img_name)     
            print(modified_data)
            file_serializer = FilesUploadSerializer(data=modified_data)
            if file_serializer.is_valid():
                file_serializer.save()
                arr.append(file_serializer.data)
            # else:
            #     flag = 0

        excel_main = {"id": 5, "excel": request.data['excel']}    

        excel_serializer = FilesUploadSerializer(data=excel_main)
        # if excel_serializer.is_valid():
        #     excel_serializer.save()

        # IPTC Function goes here
        # excel = settings.MEDIA_ROOT + "/excel/Heavy Retouch_Keywording Sample_Main.xlsx"

        # excel = FilesUpload.objects.get(id=1)
        # print(excel)

        # set_metadata = IPTCKeyword(excel)
        # set_metadata.save_metadata()
        # set_metadata.get_metadata()
        # set_metadata.get_metadata()

        zip_file_path = settings.MEDIA_ROOT + "/images.zip"

        zip_file = open(zip_file_path, 'rb')

        # print(zip_file)

        # response = HttpResponse(zip_file, content_type='application/zip')
        # response['Content-Disposition'] = 'attachment; filename=images.zip'

        # response = FileResponse(zip_file)
        response = FileResponse(zip_file, content_type="application/zip")
        response['Content-Disposition'] = 'attachment; filename=images.zip'

        # if flag == 1:
        #     return Response(arr, status=status.HTTP_201_CREATED)
        # else:
        #     return Response(arr, status=status.HTTP_400_BAD_REQUEST)

        return response
        # return Response({"status": 200})