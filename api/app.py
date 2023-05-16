from flask import Flask, request, jsonify, send_file, make_response
from core import dir_tree, save_file_due_to_context
import os
import logging


logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='api.log',
    filemode='a',
    level=logging.INFO
)

app = Flask(__name__)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE = os.path.join(BASE_DIR, 'storage')


@app.route('/upload', methods=['POST', 'GET', 'PUT'])
def upload_file():
    logging.info(f'req: {request.method}, '
                 f'form: {dict(request.form)}, '
                 f'is_file: {True if request.files else None}')
    file_path = request.form.get('file_path', default='')
    raw = request.form.get('raw', default=False)
    if file_path and not file_path.startswith('/'):
        file_path = '/' + file_path
    response = {'file_path': file_path}

    if request.method == 'POST':
        try:
            folders = '/'.join(file_path.split('/')[:-1])
            os.makedirs(STORAGE + folders,
                        exist_ok=True)
            try:
                response, data = save_file_due_to_context(
                    request, response, STORAGE, file_path)
                response.update({'data': data})
            except UnboundLocalError:
                response.update({'data': "can't decode preview"})

        except Exception as e:
            logging.error(e)
            response.update({
                'error': 'There is an error with your POST request',
                'http_status_code': 400})

    elif request.method == 'PUT':
        try:
            response, data = save_file_due_to_context(
                    request, response, STORAGE, file_path)
            response.update({'data': data})
        except UnboundLocalError:
            response.update({'data': "can't decode preview"})
        except FileNotFoundError:
            response.update({'error': 'file does not exist',
                             'http_status_code': 404})
        except Exception as e:
            logging.error(e)
            response.update({
                'error': 'There is an error with your PUT request',
                'http_status_code': 400})

    else:
        try:
            if raw == 'yes':
                return send_file(STORAGE + file_path, as_attachment=False)
            else:
                with open(STORAGE + file_path, 'rb') as raw_file:
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
            logging.error(e)
            response.update({
                'error': 'There is an error with your GET request',
                'http_status_code': 400})

    return make_response(jsonify(response), response.get('http_status_code'))


@app.route('/dir', methods=['GET', ])
def get_dir():
    return jsonify(dir_tree(STORAGE))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6000)
