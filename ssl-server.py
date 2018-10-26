##
# ssl-server.py - A simple SSL/TLS server
#
# Author: umnagendra@gmail.com
# License: MIT (see LICENSE file)
##

import sys
# exit if not python 3
if sys.version_info <= (3, 0):
    sys.exit('FATAL: Requires python 3')

import argparse
import logging
import socket
import ssl

# CONSTANTS
DEFAULT_CIPHERS = 'EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH'
SOCKET_BACKLOG = 5

# log to STDOUT with a decent timestamp
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s: %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def process_args():
    argParser = argparse.ArgumentParser(description='Simple SSL/TLS server')
    argParser.add_argument('--host', help='Fully Qualified Hostname / IP of this server', required=True)
    argParser.add_argument('--port', help='64-bit UNIX port for the server to listen on', type=int, required=True)
    argParser.add_argument('--certFile', help='Path to server certificate file (in PEM format)', required=True)
    argParser.add_argument('--keyFile', help='Path to private key file (in PEM format)', required=True)
    argParser.add_argument('--keyPass', help='Password to access private key (if private key file is encrypted)', default=None, required=False)
    argParser.add_argument('--ciphers', help='Supported ciphers', default=DEFAULT_CIPHERS, required=False)
    return vars(argParser.parse_args())


def handle(connection):
    logging.info(connection.recv())
    # simply returning a HTTP 200 OK so even browsers can act as clients and test this server
    # does NOT mean this is a HTTP server, though (it cannot understand any HTTP methods etc.)
    connection.write(b'HTTP 1.1 200 OK\n\n%s' % connection.getpeername()[0].encode())


def create_socket(host, port, certFile, keyFile, keyPass, ciphers):
    sock = socket.socket()
    sock.bind((host, port))
    sock.listen(5)
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certFile, keyFile, keyPass)
    context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
    context.set_ciphers(ciphers)    
    return (sock, context)


def run_server(socket, context):
    logging.info('Starting server ...')
    while True:
        connection = None
        serversock, _ = socket.accept()
        try:
            logging.info('Handling incoming connection ...')
            connection = context.wrap_socket(serversock, server_side=True)
            handle(connection)
        except ssl.SSLError as e:
            logging.error('SSLError', exc_info=e, stack_info=True)
        finally:
            if connection:
                connection.close()


def start_server(args):
    sock, context = create_socket(args['host'], args['port'], args['certFile'], args['keyFile'], args['keyPass'], args['ciphers'])
    run_server(sock, context)


def main():
    args = process_args()
    logging.info('Running script with arguments: {}'.format(args))
    start_server(args)


if __name__ == '__main__':
    main()
