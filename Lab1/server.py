import socket
from PIL import Image
import pickle
import numpy as np
import math
from os import path
import time

class Server():
    def __init__(self, headerSize=64, bufferSize=4096):
        self.headerSize = headerSize
        self.bufferSize = bufferSize
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def bind(self, serverName, serverPort):
        self.serverSocket.bind((serverName, serverPort))

    def start(self):
        while True:
            # socket.accept(): accept a connection; conn is a new socket object usable to send and receive data
            # addr is the address bounded to the socket on the other end of the connection
            self.serverSocket.listen(1)
            try:
                connectionSocket, addr = self.serverSocket.accept()
                print("Connected by ", addr)
                self.handle_client(connectionSocket)
            except socket.error as err:
                print("Connection failed")
            connectionSocket.close()

    def handle_client(self, conn):
        msg_length = self.get_Header(conn)
        n_recvs = math.ceil(msg_length / self.bufferSize)
        full_request = []
        for i in range(n_recvs):
            msg = conn.recv(self.bufferSize).decode()
            full_request.append(msg)
        full_request = ''.join(full_request)

        self.send_response(conn, full_request)

    def get_Header(self, conn):
        msg_length = conn.recv(self.headerSize).decode()
        if msg_length:
            msg_length = int(msg_length)
        return msg_length
#
    def send_response(self, conn, file_name):
        # time.sleep(6)
        if path.exists(file_name):
            http_status = 200
            http_status_str = str(http_status) + " OK"
            if file_name.endswith(".txt"):
                file_extension = "txt"
                http_header = ("Server HTTP Response: HTTP/1.1 {}\nContent-type: {}/html\n\n").format(http_status_str, file_extension)
                file = open(file_name, mode='r')
                http_content = file.read()
                self.send(conn, http_status, http_header, http_content, file_extension)

            elif file_name.endswith(".jpg"):
                file_extension = "jpg"
                http_header = ("Server HTTP Response: HTTP/1.1 {}\nContent-type: {}/image\n\n").format(http_status_str, file_extension)
                img = Image.open(file_name)
                http_content = np.asarray(img)
                self.send(conn, http_status, http_header, http_content, file_extension)
        else:
            http_status = 404
            file_extension = "invalid"
            http_status_str = str(http_status) + " not found"
            http_header = ("Server HTTP Response: HTTP/1.1 {}\n\n").format(http_status_str)
            http_content = "404 Not Found"
            self.send(conn, http_status, http_header, http_content, file_extension)

    def send(self, conn, http_status, http_header, http_content, file_extension):
        full_response = {}
        full_response["ext"] = file_extension
        full_response["status"] = http_status
        full_response["header"] = http_header
        full_response["response"] = http_content
        pkl_response = pickle.dumps(full_response)
        response_length = len(pkl_response)
        send_length = str(response_length).encode()
        send_length += b' ' * (self.headerSize - len(send_length))
        conn.send(send_length)
        conn.send(pkl_response)



if __name__ == "__main__":

    serverPort = 12345
    serverName = 'localhost'

    server = Server()
    server.bind(serverName, serverPort)
    server.start()


