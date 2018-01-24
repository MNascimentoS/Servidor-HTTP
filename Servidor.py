
#!/usr/bin/python

import socket  # Networking support
import signal  # Signal support (server shutdown on signal receive)
import time  # Current time
import sys
import json
from Conexao import Conexao


class Servidor:
    """ Class describing a simple HTTP server objects."""

    def __init__(self, port=80):
        """ Constructor """
        self.conexao = Conexao()
        self.host = 'localhost'  # <-- works on all avaivable network interfaces
        self.port = port
        self.www_dir = 'www'  # Directory where webpage files are stored

    def run_server(self):
        """ Attempts to aquire the socket and launch the server """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:  # user provided in the __init__() port may be unavaivable
            print(" The Servidor is on: " + self.host + "Port number: " + self.port)
            self.socket.bind((self.host, self.port))

        except Exception as e:
            print("Warning: Could not aquite port: " + str(self.port) + "\n")
            print("I will try a higher port")
            # store to user provideed port locally for later (in case 8080 fails)
            user_port = self.port
            self.port = 8000

            try:
                print(" The Servidor is on: " + self.host + " Port number: " + str(self.port))
                self.socket.bind((self.host, self.port))

            except Exception as e:
                print("ERROR: Failed to acquire sockets for ports " + str(user_port) + " and 8080. ")
                print("Try running the Servidor in a privileged user mode.")
                self.shutdown()
                sys.exit(1)

        print("Waiting for requests...")
        self._wait_for_connections()

    def shutdown(self):
        """ Shut down the server """
        try:
            print("Shutting down the server")
            self.conexao.close()
            s.socket.shutdown(socket.SHUT_RDWR)

        except Exception as e:
            print("Warning: could not shut down the socket. Maybe it was already closed? " + str(e))

    def _gen_headers(self, code):
        """ Generates HTTP response Headers. Ommits the first line! """

        # determine response code
        h = ''
        if (code == 200):
            h = 'HTTP/1.1 200 OK\n'
        elif (code == 404):
            h = 'HTTP/1.1 404 Not Found\n'

        # write further headers
        current_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        h += 'Date: ' + current_date + '\n'
        h += 'Servidor: Simple-Python-HTTP-Servidor\n'
        h += 'Connection: close\n\n'  # signal that the conection wil be closed after complting the request

        return h

    def _wait_for_connections(self):
        """ Main loop awaiting connections """
        while True:
            self.socket.listen(3)  # maximum number of queued connections

            conn, addr = self.socket.accept()
            # conn - socket to client
            # addr - clients address

            print("Got connection from:" + str(addr))

            data = conn.recv(1024)  # receive data from client
            string = bytes.decode(data)  # decode it to string

            # determine request method  (HEAD and GET are supported)
            request_method = string.split(' ')[0]
            print("Method: " + request_method)
            print("Request body: " + string)

            # if string[0:3] == 'GET':
            if (request_method == 'GET') | (request_method == 'HEAD'):
                # file_requested = string[4:]

                # split on space "GET /file.html" -into-> ('GET','file.html',...)
                file_requested = string.split(' ')
                file_requested = file_requested[1]  # get 2nd element
                print("file requested: " + file_requested)

                # Check for URL arguments. Disregard them
                file_requested = file_requested.split('?')[0]  # disregard anything after '?'

                if (file_requested == '/' or file_requested == ''):  # in case no file is specified by the browser
                    file_requested = '/index.html'  # load index.html by default
                elif file_requested == "/Arduino":
                    self.conexao.sendMessage("Recebendo conexao: "+str(addr))
                    response_headers = self._gen_headers(200)
                    server_response = response_headers.encode()
                    conn.send(server_response)
                    print("Closing connection with client")
                    conn.close()
                    continue
                elif file_requested == "/Temperatura":
                    response_headers = self._gen_headers(200)
                    server_response = response_headers.encode()
                    server_response += self.conexao.getTemperature().encode()
                    conn.send(server_response)
                    print("Closing connection with client")
                    conn.close()
                    continue
                else:
                    file_requested = '/' + file_requested

                file_requested = self.www_dir + file_requested
                print("Serving web page [" + file_requested + "]")

                ## Load file content
                try:
                    file_handler = open(file_requested, 'rb')
                    if (request_method == 'GET'):  # only read the file when GET
                        response_content = file_handler.read()  # read file content
                    file_handler.close()

                    response_headers = self._gen_headers(200)

                except Exception as e:  # in case file was not found, generate 404 page
                    print("Warning, file not found. Serving response code 404\n", e)
                    response_headers = self._gen_headers(404)
                    if (request_method == 'GET'):
                        file_requested = self.www_dir + "/error404.html"
                        file_handler = open(file_requested, 'rb')
                        response_content = file_handler.read()
                        file_handler.close()

                server_response = response_headers.encode()  # return headers for GET and HEAD
                if (request_method == 'GET'):
                    server_response += response_content  # return additional conten for GET only
                conn.send(server_response)
                print("Closing connection with client")
                conn.close()
            elif (request_method == 'POST'):
                self.conexao.sendMessage(str(addr))
                response_headers = self._gen_headers(200)
                server_response = response_headers.encode()
                server_response += self.conexao.getTemperature().encode()
                conn.send(server_response)
                print("Closing connection with client")
                conn.close()
            else:
                print("Unknown HTTP request method:", request_method)


def graceful_shutdown(sig, dummy):
    """ This function shuts down the server. It's triggered
    by SIGINT signal """
    s.shutdown()  # shut down the server
    sys.exit(1)


###########################################################
# shut down server on ctrl+c
signal.signal(signal.SIGINT, graceful_shutdown)

if __name__ == '__main__':
    print("Hello, I am starting http server...")
    s = Servidor(80)  # construct server object
    s.run_server()  # aquire the socket