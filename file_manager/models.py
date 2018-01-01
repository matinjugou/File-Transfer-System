from django.db import models

__author__ = "Bifei Yang"


class myFile(models.Model):
    fileType = models.CharField(max_length=128)
    validTime = models.IntegerField()
    fileUrl = models.CharField(max_length=256)
    uploadTime = models.DateField(auto_now_add=True)
    file = models.FileField(upload_to='files/%Y/%m/%d')
    image = models.ImageField(upload_to='images/%Y/%m/%d', blank=True, null=True)
    imageUrl = models.CharField(max_length=256, default='')


class myRobot(models.Model):
    fileType = models.CharField(max_length=128)
    fileUrl = models.CharField(max_length=256)
    uploadTime = models.DateField(auto_now_add=True)
    file = models.FileField(upload_to='robots')
    companyId = models.IntegerField()
