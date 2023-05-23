from django.urls import path
from files.views import index


urlpatterns = [
    path('upload', index)
]