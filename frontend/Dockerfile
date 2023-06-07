FROM python:3.10
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt --no-cache-dir
RUN python3 manage.py migrate
CMD ["gunicorn", "my_storage_gui.wsgi:application", "--bind", "0:8000"]
