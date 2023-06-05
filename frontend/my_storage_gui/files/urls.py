from django.urls import path
from files.views import index, download, upload

app_name = 'files'


urlpatterns = [
    path('', index, name='index'),
    path('my_storage/download/<path:path>', download, name='download'),
    path('my_storage/upload/<path:path>', upload, name='upload')
]
