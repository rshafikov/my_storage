import json
import logging
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STORAGE = os.path.join(BASE_DIR, 'storage')

logging.basicConfig(
    format='%(asctime)s | %(levelname)s | %(message)s',
    filename=os.path.join(BASE_DIR, 'api.log'),
    filemode='a',
    level=logging.INFO
)


def dir_tree(path):
    tree = {}
    contents = os.listdir(path)
    for item in contents:
        full_path = os.path.join(path, item)
        if os.path.isdir(full_path):
            tree.update({item: dir_tree(full_path)})
            continue
        tree.update({item: 'file'})
    return tree


def save_file_due_to_context(request, response, file_path):
    if request.files:
        request.files['file'].save(STORAGE + file_path)
    else:
        data = request.form.get('text')
        with open(STORAGE + file_path, 'w') as file:
            file.write(data)
    response.update({'storage_tree': dir_tree(STORAGE),
                     'http_status_code': 200})
    return response, data


def main():
    print(json.dumps(
        dir_tree(input('Enter dir path: ')),
        indent=4))


if __name__ == '__main__':
    main()
