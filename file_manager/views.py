from basic.base import BaseView
from file_manager.models import myFile
from file_manager.forms import FileForm
from file_service import settings

from django.http import HttpResponse
from django.shortcuts import render

import json

__author__ = "Bifei Yang"


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

        new_file.fileUrl = settings.CONFIGS['SITE_DOMAIN'] + ":8000" + new_file.file.url

        return HttpResponse(json.dumps({
            'code': 0,
            'msg': "",
            'data': new_file.fileUrl
        }), content_type="application/json")

    def get(self):
        files = myFile.objects.all()
        form = FileForm()
        return render(self.request, 'fileList.html', {'files': files, 'form': form})