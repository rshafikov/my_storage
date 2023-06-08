[![my_storage_CI](https://github.com/rshafikov/my_storage/actions/workflows/main.yml/badge.svg)](https://github.com/rshafikov/my_storage/actions/workflows/main.yml)

## My_storage

This is a simple storage to keep your files. You can upload/download any data you want just in few seconds.

You can write path to file, file content or select file to upload. Click [it](http://52.59.62.239/) to try. 

## Api endpoints

1. [my_storage/api/dir](http://52.59.62.239/api/dir) <- current file tree of your storage

    METHODS: GET<br>

    Curl example: `curl my_storage_ip/api/dir`

2. [my_storage/api/upload](http://52.59.62.239/api/upload?path=test_file.txt&raw=yes) <- click to download test_file.txt<br>

    METHODS: GET<br>

    ARGS:<br>

    path='path/to/file' - file's path you want to download;<br>

    raw='yes' - if you want to get the file as file not as a text;<br> 

    Curl example: `curl -X GET -d 'path=test_dir/test_file_via_curl' my_storage_ip/api/upload`

3. [my_storage/api/upload](http://52.59.62.239/api/upload?path=test_dir/test_file_via_curl) <- resourse to upload files or text

    METHODS: POST, PUT<br>

    ARGS:<br>

    path='path/to/file' - file's path you want to upload;<br>

    text='text' - file text;<br>

    or<br>

    file='@file' - chosen file;<br>

    Curl example with text: `curl -X POST -d 'path=test_dir/test_file_via_curl' -d 'text=test text' my_storage_ip/api/upload`<br>

    Curl example with file: `curl -X POST -F 'path=secret_files/hot_mom_stuck_in_washing_machine.mp4' -F 'file=@test_file_to_upload' my_storage_ip/api/upload`

## How to deploy:

```bash
# Clone it
git clone https://github.com/rshafikov/my_storage.git
# Change work directory
cd my_storage/deploy/
# Create env file with your options
cat > .env
# FRONTEND_DEBUG='False' or 'True' - skipable
# API_URL_REDIRECT='your server white IP' - necessarily
# ALLOWED_HOSTS='*' change this if you want more safety - skipable

# Run it, but idk how you will install docker compose, not my business
sudo docker compose up -d
# Upload your first file via curl
curl -X POST -d 'path=test_dir/test_file_via_curl' -d 'text=Hello World!' your_server_white_IP/api/upload
```
