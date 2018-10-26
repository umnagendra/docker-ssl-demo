FROM python:alpine3.7

WORKDIR /ssl-server
COPY ssl-server.py /ssl-server/

# The 'host' argument shall always be 0.0.0.0 to map to all IPs inside the container
CMD python ./ssl-server.py --host 0.0.0.0 --port ${PORT} --certFile ${CERTFILE} --keyFile ${KEYFILE} --keyPass ${KEYPASS}
EXPOSE ${PORT}
