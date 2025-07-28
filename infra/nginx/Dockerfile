FROM nginx:stable
EXPOSE 80
COPY ./static/ /usr/share/nginx/html/static/
COPY ./pages/ /usr/share/nginx/html/static/pages/error/
COPY ./favicon.ico /usr/share/nginx/html/favicon.ico
COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./app.conf.template /etc/nginx/app.conf.template
ENV DOLLAR='$'

CMD [ "/bin/bash", "-c", "envsubst < /etc/nginx/app.conf.template > /etc/nginx/conf.d/app.conf && nginx -g 'daemon off;'" ]