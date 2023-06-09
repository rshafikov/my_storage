import logging
import os
import traceback

from core import STORAGE, dir_tree, logging, save_file_due_to_context
from flask import Flask, jsonify, make_response, request, send_file

app = Flask(__name__)


@app.route('/upload', methods=['POST', 'GET', 'PUT'])
def upload_file():
    logging.info(
        f'req_method: {request.method}, '
        f'root_url: {request.url}, '
        f'form: {dict(request.form)}, '
        f'is_file: {True if request.files else None}, '
        f'client_addr: {request.remote_addr}')
    path = request.args.get('path', '', str) or (
        request.form.get('path', '', str))
    raw = request.args.get('raw', 'no', str) or (
        request.form.get('raw', 'no', str))
    path = '/' + path if (path and not path.startswith('/')) else path
    response = {'path': path}

    if request.method == 'POST':
        try:
            folders = '/'.join(path.split('/')[:-1])
            os.makedirs(STORAGE + folders,
                        exist_ok=True)
            try:
                response, data = save_file_due_to_context(
                    request, response, path)
                response.update({'data': data})
            except UnboundLocalError:
                response.update({'data': "can't decode preview"})

        except Exception as e:
            logging.error('{}{}'.format(traceback.format_exc(), e))
            response.update({
                'error': 'There is an error with your POST request',
                'http_status_code': 400})

    elif request.method == 'PUT':
        try:
            response, data = save_file_due_to_context(
                request, response, path)
            response.update({'data': data})
        except UnboundLocalError:
            response.update({'data': "can't decode preview"})
        except FileNotFoundError:
            response.update({'error': 'file does not exist',
                             'http_status_code': 404})
        except Exception as e:
            logging.error('{}{}'.format(traceback.format_exc(), e))
            response.update({
                'error': 'There is an error with your PUT request',
                'http_status_code': 400})

    else:
        try:
            if raw == 'yes':
                return send_file(STORAGE + path, as_attachment=True)
            else:
                with open(STORAGE + path, 'rb') as raw_file:
                    last_raw_data = raw_file.read()
                    response.update({'data': last_raw_data.decode('utf-8'),
                                     'http_status_code': 200})
        except UnicodeDecodeError:
            response.update({'data': "can't decode preview",
                             'http_status_code': 200})
        except FileNotFoundError:
            response.update({'error': 'file does not exist',
                             'http_status_code': 404})
        except TypeError:
            response.update({'error': 'empty body',
                             'http_status_code': 400})
        except Exception as e:
            logging.error('{}{}'.format(traceback.format_exc(), e))
            response.update({
                'error': 'There is an error with your GET request',
                'http_status_code': 400})

    return make_response(jsonify(response), response.get('http_status_code'))


@app.route('/dir', methods=['GET', ])
def get_dir():
    logging.info(
        f'root_path: {request.root_url}, '
        f'client_addr: {request.remote_addr}')
    return jsonify(dir_tree(STORAGE))


if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=int(os.getenv('API_PORT', default='5000'))
    )
