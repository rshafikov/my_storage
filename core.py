import os
import json


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


def main():
    print(json.dumps(
        dir_tree(input('Enter dir path: ')),
        indent=4))


if __name__ == '__main__':
    main()
