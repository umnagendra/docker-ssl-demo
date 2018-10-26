# docker-ssl-demo
Demo SSL server to test TLS connections into a docker container

## Build
1. Clone the repo

2. Build and install the docker image in the local repo
    ```
    docker build -t ssl-server <PATH_TO_REPO_DIR>
    ```

3. Optionally, the image can be exported into a portable TARball
    ```
    docker save -o ssl-server_latest.tar ssl-server
    ```

## Run
### Generate private key and SSL certificate
Use OpenSSL to generate a private key and SSL certificate on the host machine.
```
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365
```
![image](https://user-images.githubusercontent.com/990210/47568776-9d546e00-d94f-11e8-8301-1cca73a8d789.png)

### Run the container
Mount the directory containing generated private key and SSL certificate as a volume, and start a container as a daemon.

```
docker run -d -p <PORT ON HOST>:<PORT IN CONTAINER> \
-e "PORT=<PORT IN CONTAINER>" \
-e "CERTFILE=/certs/cert.pem" \
-e "KEYFILE=/keys/key.pem" \
-e "KEYPASS=12Ccbu12" \
--volume "<ABSOLUTE PATH TO DIR CONTAINING GENERATED SSL CERT>:/certs" \
--volume "<ABSOLUTE PATH TO DIR CONTAINING GENERATED PRIVATE KEY>:/keys" \
--name ssl-server ssl-server
```
Logs can be viewed / tailed using `docker logs --tail ssl-server`

## Test
You can use an SSL client to verify the SSL handshake, certificate, cipher negotiations etc.
```
openssl s_client -connect <HOST_IP>:<HOST_PORT> -tls1_2
```

Alternately, you can also use a HTTPS client (like cURL or a browser) - the server always serves back a basic HTTP 200 OK response.

![image](https://user-images.githubusercontent.com/990210/47569706-eb6a7100-d951-11e8-8141-fc81aedb75d1.png)
