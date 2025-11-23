FROM python:3.11-slim
LABEL maintainer="Dmitry Titenkov <lt200711@yandex.ru>"
LABEL version="1.0"
LABEL description="API for booking hotel rooms"
RUN mkdir /app
COPY  requirements.txt /app
RUN pip3 install -r /app/requirements.txt --no-cache-dir -vvv
COPY . /app
WORKDIR /app
CMD [ "gunicorn", "bookinn.wsgi:application", "--bind", "0.0.0.0:8000" ]