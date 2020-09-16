import socket
from PIL import Image
import pickle
import numpy as np
import math
from os import path

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
            connectionSocket, addr = self.serverSocket.accept()
            self.handle_client(connectionSocket)
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
        full_response = {}
        if path.exists(file_name):
            http_status = 200
            full_response["status"] = http_status
            http_status_str = str(http_status) + " OK"
            if file_name.endswith(".txt"):
                file_extension = "txt"
                full_response["ext"] = file_extension
                http_header = ("Server HTTP Response: HTTP/1.1 {}\nContent-type: {}/html\n\n").format(http_status_str, file_extension)
                file = open(file_name, mode='r')
                file_content = file.read()
                full_response["header"] = http_header
                full_response["response"] = file_content
                pkl_response = pickle.dumps(full_response)
                response_length = len(pkl_response)
                send_length = str(response_length).encode()
                send_length += b' '*(self.headerSize - len(send_length))
                conn.send(send_length)
                conn.send(pkl_response)

            elif file_name.endswith(".jpg"):
                file_extension = "jpg"
                full_response["ext"] = file_extension
                http_header = ("Server HTTP Response: HTTP/1.1 {}\nContent-type: {}/image\n\n").format(http_status_str, file_extension)
                img = Image.open(file_name)
                img_arr = np.asarray(img)
                full_response["header"] = http_header
                full_response["response"] = img_arr
                pkl_response = pickle.dumps(full_response)
                response_length = len(pkl_response)
                send_length = str(response_length).encode()
                send_length += b' '*(self.headerSize - len(send_length))
                conn.send(send_length)
                conn.send(pkl_response)
        else:
            http_status = 404
            full_response["status"] = http_status
            full_response["ext"] = "None"
            http_status_str = str(http_status) + " not found"
            http_header = ("Server HTTP Response: HTTP/1.1 {}\n\n").format(http_status_str)
            response = "404 Not Found"
            full_response["header"] = http_header
            full_response["response"] = response
            pkl_response = pickle.dumps(full_response)
            response_length = len(pkl_response)
            send_length = str(response_length).encode()
            send_length += b' ' * (self.headerSize - len(send_length))
            conn.send(send_length)
            conn.send(pkl_response)


if __name__ == "__main__":

    serverPort = 12346
    serverName = 'localhost'

    server = Server()
    server.bind(serverName, serverPort)
    server.start()


