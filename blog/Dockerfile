FROM python:3.12.3 AS hugo
WORKDIR /deploy

RUN pip install hugo==0.153.0

COPY hugo/ hugo/
RUN cd /deploy/hugo && hugo --minify

FROM nginx:latest
COPY --from=hugo /deploy/hugo/public /usr/share/nginx/html/blog
