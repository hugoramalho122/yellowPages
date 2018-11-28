FROM nginx:stable

RUN apt-get update
RUN apt-get install -y ca-certificates

COPY config /etc/nginx

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]