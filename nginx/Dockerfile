FROM nginx:latest

RUN mkdir -p /code/staticfiles

RUN mkdir -p /code/media
RUN mkdir -p /code/media/services
RUN mkdir -p /code/media/menu
RUN mkdir -p /code/media/personnel
RUN mkdir -p /code/media/meals

COPY ./nginx.conf /etc/nginx/nginx.conf

EXPOSE 8080