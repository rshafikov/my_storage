FROM python:3.10
RUN mkdir /app
COPY ./*.py /app
COPY requirements.txt /app
WORKDIR /app
RUN pip3 install -r requirements.txt --no-cache-dir
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
