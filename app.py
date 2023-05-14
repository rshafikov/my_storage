from flask import Flask, request, jsonify, send_file, make_response
from core import dir_tree
import os


app = Flask(__name__)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE = os.path.join(BASE_DIR, 'storage')


@app.route('/upload', methods=['POST', 'GET', 'PUT'])
def upload_file():
    file_path = request.form.get('file_path', default='')
    raw = request.form.get('raw', default=False)
    if file_path and not file_path.startswith('/'):
        file_path = '/' + file_path
    answer = {'file_path': file_path}

    if request.method == 'POST':
        try:
            folders = '/'.join(file_path.split('/')[:-1])
            os.makedirs(STORAGE + folders,
                        exist_ok=True)
            if request.files:
                data, data_type = request.files['file'].read(), 'wb'
            else:
                data, data_type = request.form.get('file'), 'w'
            with open(STORAGE + file_path, data_type) as raw_file:
                raw_file.write(data)
                answer.update({'storage_tree': dir_tree(STORAGE)})
                try:
                    answer.update({'data': data.decode('utf-8'),
                                   'http_status_code': 200})
                except AttributeError:
                    answer.update({'data': data,
                                   'http_status_code': 200})
                except UnicodeDecodeError:
                    answer.update({'data': "can't decode preview",
                                   'http_status_code': 200})
        except Exception:
            answer.update({'error': 'There is an error with your POST request',
                           'http_status_code': 400})

    elif request.method == 'PUT':
        try:
            if request.files:
                data, data_type = request.files['file'].read(), 'wb'
                answer.update({'data': data.decode('utf-8')})
            else:
                data, data_type = request.form.get('file'), 'w'
                answer.update({'data': data})
            with open(STORAGE + file_path, data_type) as raw_file:
                raw_file.write(data)
        except FileNotFoundError:
            answer.update({'error': 'file does not exist',
                           'http_status_code': 404})
        except Exception:
            answer.update({'error': 'There is an error with your PUT request',
                           'http_status_code': 400})

    else:
        try:
            if raw == 'yes':
                return send_file(STORAGE + file_path, as_attachment=False)
            else:
                with open(STORAGE + file_path, 'rb') as raw_file:
                    last_raw_data = raw_file.read()
                    answer.update({'data': last_raw_data.decode('utf-8'),
                                   'http_status_code': 200})
        except UnicodeDecodeError:
            answer.update({'data': "can't decode preview",
                           'http_status_code': 200})
        except FileNotFoundError:
            answer.update({'error': 'file does not exist',
                           'http_status_code': 404})
        except TypeError:
            answer.update({'error': 'empty body',
                           'http_status_code': 400})
        except Exception:
            answer.update({'error': 'There is an error with your GET request',
                           'http_status_code': 400})

    return make_response(jsonify(answer), answer.get('http_status_code'))


@app.route('/dir', methods=['GET', ])
def get_dir():
    return jsonify(dir_tree(STORAGE))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
