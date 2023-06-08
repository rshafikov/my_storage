from django.shortcuts import render, redirect
import requests
from my_storage_gui.settings import API_INTERNAL_IP, API_EXTERNAL_IP_REDIRECT
import json


def download(request, path):
    try:
        raw = (('?' + request.GET.get('download') + '=yes') if (
            request.GET.get('download')) else '')
        if raw:
            return redirect(
                f'http://{API_EXTERNAL_IP_REDIRECT}/upload{raw}&path={path}')
        dir_tree = requests.get(f'{API_INTERNAL_IP}/dir').json()
        api_response = requests.get(
            f'{API_INTERNAL_IP}/upload', data={'path': path}).json()
    except requests.RequestException as error:
        api_response = {
            'data': type(error).__name__,
            'error_message': str(error)
        }
        dir_tree = {'error': 'Unavailable'}
    content = api_response.get('data') or api_response.get('error')

    return render(
        request,
        template_name='api_response.html',
        context={
            'response': json.dumps(api_response, indent=4),
            'dir_tree': json.dumps(dir_tree, indent=4),
            'content': content if len(content) <= 30 else (
                'Large file. Please download it instead.'),
            'path': path
        }
    )


def upload(request, path):
    file = request.FILES.get('file')
    text = request.POST.get('text', 'empty file content')
    api_response = {'error': text}
    try:
        if file:
            api_response = requests.post(
                f'{API_INTERNAL_IP}/upload',
                files={'file': file},
                data={'path': path}).json()
        else:
            api_response = requests.post(
                f'{API_INTERNAL_IP}/upload',
                data={'path': path, 'text': text}).json()
        dir_tree = requests.get(f'{API_INTERNAL_IP}/dir').json()
    except requests.RequestException as error:
        dir_tree = {'error': 'Unavailable'}
        api_response = {
            'exception_type': type(error).__name__,
            'error_message': str(error)
        }
    return render(
        request,
        template_name='api_response.html',
        context={
            'response': json.dumps(api_response, indent=4),
            'dir_tree': json.dumps(dir_tree, indent=4),
            'content': file if file else text
        }
    )


def index(request):
    return render(request, template_name='index.html')
