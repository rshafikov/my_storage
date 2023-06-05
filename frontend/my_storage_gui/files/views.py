from django.shortcuts import render, redirect
from django.http import FileResponse
import requests
from my_storage_gui.settings import API_URL
import json


def index(request):
    path = request.POST.get('path')
    if request.POST.get('action') == 'upload' and path:
        request.session['text'] = request.POST.get('text')
        return redirect('files:upload', path)
    elif request.POST.get('action') == 'download' and path:
        return redirect('files:download', path)

    return render(request, template_name='index.html')


def download(request, path):
    try:
        raw = (
            ('?' + request.GET.get('download') + '=yes') if (
                request.GET.get('download')) else '')
        if raw:
            return redirect(f'{API_URL}/upload{raw}&path={path}')
        api_response = requests.get(
            f'{API_URL}/upload', data={'path': path}).json()
        dir_tree = requests.get(f'{API_URL}/dir').json()
    except requests.RequestException as error:
        api_response = {
            'exception_type': type(error).__name__,
            'error_message': str(error)
        }
        dir_tree = {'error': 'Unavailable'}

    return render(
        request,
        template_name='api_response.html',
        context={
            'response': json.dumps(api_response, indent=4),
            'dir_tree': json.dumps(dir_tree, indent=4),
            'content': api_response.get('data'),
            'path': path}
    )


def upload(request, path):
    text = request.session.pop('text', 'Please follow to home page.')
    try:
        api_response = {'error': text}
        if text != 'Please follow to home page.':
            api_response = requests.post(
                f'{API_URL}/upload', data={'path': path, 'text': text}).json()
        dir_tree = requests.get(f'{API_URL}/dir').json()
    except Exception('There is error on the back side') as error:
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
            'content': text
        }
    )
