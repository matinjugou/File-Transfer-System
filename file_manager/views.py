from basic.base import BaseView
from file_manager.models import myFile
from file_manager.forms import FileForm
from file_service import settings

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.shortcuts import render

import json

__author__ = "Bifei Yang"

@method_decorator(csrf_exempt, name='dispatch')
class FileView(BaseView):
    def post(self):
        self.check_input('fileType', 'validTime')
        new_file = myFile(
            fileType=self.input['fileType'],
            validTime=self.input['validTime'],
            fileUrl='',
            file=self.request.FILES['file']
        )
        new_file.save()

        new_file.fileUrl = settings.CONFIGS['SITE_DOMAIN'] + new_file.file.url
        response =  HttpResponse(json.dumps({
            'code': 0,
            'msg': "",
            'data': new_file.fileUrl
        }), content_type="application/json")
        return response

    def get(self):
        files = myFile.objects.all()
        form = FileForm()
        return render(self.request, 'fileList.html', {'files': files, 'form': form})
