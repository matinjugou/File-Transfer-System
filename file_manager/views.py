from basic.base import BaseView
from file_manager.models import myFile, myRobot
from file_manager.forms import FileForm, ImageForm
from file_manager.AnsMake import find_answer, check_file
from file_service import settings

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile

import json
from io import BytesIO

__author__ = "Bifei Yang"


@method_decorator(csrf_exempt, name='dispatch')
class FileView(BaseView):
    def post(self):
        try:
            self.check_input('fileType', 'validTime')
        except Exception:
            response = HttpResponseBadRequest()
            return response

        if self.request.FILES['file'].size > 10500000:
            response = HttpResponseBadRequest('The file is too large!')
            return response

        new_file = myFile(
            fileType=self.input['fileType'],
            validTime=self.input['validTime'],
            fileUrl='',
            file=self.request.FILES['file']
        )
        new_file.save()

        new_file.fileUrl = settings.CONFIGS['SITE_DOMAIN'] + new_file.file.url
        response = HttpResponse(json.dumps({
            'code': 0,
            'msg': "",
            'data': new_file.fileUrl
        }), content_type="application/json")
        return response

    def get(self):
        files = myFile.objects.all()
        form = FileForm()
        return render(self.request, 'fileList.html', {'files': files, 'form': form})


@method_decorator(csrf_exempt, name='dispatch')
class FileView2(BaseView):
    def post(self):
        try:
            self.check_input('validTime')
        except Exception:
            response = HttpResponseBadRequest()
            return response

        if self.request.FILES['file'].size > 10500000:
            response = HttpResponseBadRequest('The file is too large!')
            return response

        new_file = myFile(
            fileType='',
            validTime=self.input['validTime'],
            fileUrl='',
            file=self.request.FILES['file'],
        )
        new_file.save()
        new_file.file.close()

        new_file.fileType = self.request.FILES['file'].content_type
        new_file.fileUrl = settings.CONFIGS['SITE_DOMAIN'] + new_file.file.url
        new_file.save()

        response = HttpResponse(json.dumps({
            'code': 0,
            'msg': "",
            'data': new_file.fileUrl,
            'type': new_file.fileType
        }), content_type="application/json")
        return response

    def get(self):
        files = myFile.objects.all()
        form = FileForm()
        return render(self.request, 'fileList2.html', {'files': files, 'form': form})


@method_decorator(csrf_exempt, name='dispatch')
class ImageView(BaseView):
    def post(self):
        try:
            self.check_input('fileUrl')
        except Exception:
            response = HttpResponseBadRequest()
            return response

        url = self.input['fileUrl']
        start_index = url.find('/media')
        check_index = url.find(settings.CONFIGS['SITE_DOMAIN'])
        if start_index < 0 or check_index < 0:
            response = HttpResponseBadRequest('file not on this server')
            return response

        try:
            m_file = myFile.objects.filter(fileUrl=url)[0]
        except IndexError:
            notice = "this file has no attribute: fileUrl, please upload a new file to try this service"
            return HttpResponseBadRequest(notice)

        if m_file.image is not None and m_file.imageUrl != '':
            file_url = m_file.imageUrl
        else:
            try:
                im = Image.open(m_file.file)
                width = im.width
                height = im.height
                w_rate = width / 150
                h_rate = height / 150

                if w_rate >= 1 and h_rate >= 1:
                    if w_rate > h_rate:
                        new_width = int(width / w_rate)
                        new_height = int(height / w_rate)
                    else:
                        new_width = int(width / h_rate)
                        new_height = int(height / h_rate)

                    new_image = im.resize((new_width, new_height))
                    buffer = BytesIO()
                    new_image.save(fp=buffer, format=im.format)
                    pillow_image = ContentFile(buffer.getvalue())

                    m_file.image = InMemoryUploadedFile(
                        pillow_image,
                        None,
                        m_file.file.name,
                        'image/jpeg',
                        pillow_image.tell,
                        None
                    )
                    im.close()
                    m_file.save()

                    file_url = settings.CONFIGS['SITE_DOMAIN'] + m_file.image.url
                    m_file.imageUrl = file_url
                    m_file.save()
                else:
                    file_url = m_file.fileUrl
                    m_file.imageUrl = file_url
                    m_file.image = m_file.file
                    m_file.save()
            except IOError:
                notice = "cannot create thumbnail for " + url
                # print(notice)
                return HttpResponseBadRequest(notice)
            except FileNotFoundError:
                notice = "cannot open file:" + url
                # print(notice)
                return HttpResponseBadRequest(notice)

        file_type = m_file.fileType

        response = HttpResponse(json.dumps({
            'code': 0,
            'msg': "",
            'data': file_url,
            'type': file_type
        }), content_type="application/json")
        return response

    def get(self):
        form = ImageForm()
        return render(self.request, 'ImageCompress.html', {'form': form})

@method_decorator(csrf_exempt, name='dispatch')
class RobotView(BaseView):
    def post(self):
        try:
            self.check_input('companyId')
        except Exception:
            response = HttpResponseBadRequest()
            return response

        if "text" not in self.request.FILES['file'].content_type:
            response = HttpResponseBadRequest("Format error, please upload txt file")
            return response

        companyId = self.input['companyId']
        robot_txt = myRobot.objects.filter(companyId=companyId)
        if len(robot_txt) != 0:
            robot_txt[0].file = self.request.FILES['file']
            robot_txt[0].save()
            new_file = robot_txt[0]
            new_file.fileUrl = settings.CONFIGS['SITE_DOMAIN'] + new_file.file.url
            new_file.save()
        else:
            new_file = myRobot(
                fileType='',
                fileUrl='',
                file=self.request.FILES['file'],
                companyId=self.input['companyId']
            )
            new_file.save()
            new_file.file.close()

            new_file.fileType = self.request.FILES['file'].content_type
            new_file.fileUrl = settings.CONFIGS['SITE_DOMAIN'] + new_file.file.url
            new_file.save()

        res = check_file(new_file.file)
        if res['code'] == 0:
            response = HttpResponse(json.dumps({
                'code': 0,
                'msg': "",
                'data': new_file.fileUrl,
                'type': new_file.fileType
            }), content_type="application/json")
        else:
            response = HttpResponse(json.dumps(res), content_type="application/json")

        return response

    def get(self):
        try:
            self.check_input('question', 'companyId')
        except Exception:
            response = HttpResponseBadRequest()
            return response

        companyId = self.input['companyId']
        robot_txt = myRobot.objects.filter(companyId=companyId)
        question = self.input['question']

        if len(robot_txt) == 1:
            try:
                result = find_answer(question, robot_txt[0].file.url)
                response = HttpResponse(json.dumps({
                    'code': 0,
                    'msg': "",
                    'data': result
                }), content_type="application/json")
            except Exception as e:
                response = HttpResponse(json.dumps({
                    'code': -1,
                    'msg': str(e),
                    'data': ""
                }), content_type="application/json")

            return response
        else:
            response = HttpResponse(json.dumps({
                'code': -1,
                'msg': "Robot txt is not uploaded",
                'data': ""
            }), content_type="application/json")

            return response