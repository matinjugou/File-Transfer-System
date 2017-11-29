from django.conf.urls import url
from file_manager.views import FileView

urlpatterns = [
    url(r'file/$', FileView.as_view(), name="file")
]