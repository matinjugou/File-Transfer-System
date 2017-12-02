from django.conf.urls import url
from file_manager.views import FileView, FileView2

urlpatterns = [
    url(r'v1/file/$', FileView.as_view(), name="file"),
    url(r'v2/file/$', FileView2.as_view(), name="file2")
]