from ClientHandlers import InitRequestHandler
from ClientHandlers import MoveRequestHandler
from ClientHandlers import EndRequestHandler
import socket
import logging
import os
import json


class EchoClient:
    def __init__(self, address, port, data_size):
        self.data_size=data_size
        self._create_socket()
        self._connect_to_server(address,port)
        self.send_message()


    def send_message(self):
        dictionary = {'INIT_REQ': InitRequestHandler(), 'MOVE_REQ': MoveRequestHandler(), 'END_REQ': EndRequestHandler()}
        while True:
            json_response = self.sock.recv(1024)
            request = json.loads(json_response)
            str_label = request['label']
            logging.info("Got: "+str_label+".")
            try:
                dictionary[str_label].handle(self.sock,request)
            except KeyError:
                continue

    def _create_socket(self):
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def _connect_to_server(self,address,port):
        server_address=(address,port)
        if os.path.isfile("ClientLogs.log"):
            os.unlink("ClientLogs.log")
        logging.basicConfig(filename="ClientLogs.log",level=logging.INFO)
        print("Connecting to port:  "+str(port))
        logging.info("Connected to port: "+str(port))
        self.sock.connect(server_address)

if __name__=="__main__":
    host='localhost'
    port=42012
    data_size=1024
    server=EchoClient(host, port,data_size)


