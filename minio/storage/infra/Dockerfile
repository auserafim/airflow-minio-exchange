FROM minio/minio:latest

WORKDIR /app

EXPOSE 9000 9001

CMD ["minio", "server", "/data", "--console-address", ":9001"]
