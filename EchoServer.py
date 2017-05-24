from ServerHandlers import InitRequest
from ServerHandlers import InitResponseHandler
from ServerHandlers import MoveRequest
from ServerHandlers import EndRequest
from ServerHandlers import GomokuInitRequest
from ServerHandlers import MoreLessInitRequest
from ServerHandlers import GomokuMoveResponseHandler
from ServerHandlers import MoreLessMoveResponseHandler
import socket
import logging
import os
import json


class EchoServer:
    def __init__(self, address, port, data_size):
        self.data_size=data_size
        self._create_socket()
        self._bind_socket(address,port)
        self.state=0
        if os.path.isfile("ServerLogs.log"):
            os.unlink("ServerLogs.log")
        logging.basicConfig(filename="ServerLogs.log",level=logging.INFO)

    def state_machine(self):
        self.sock.listen()
        connection, client_address=self.sock.accept()
        logging.info("Player no" + str(client_address) + " successfully connected.")
        dictionary = {'INIT_REQ': InitRequest(connection), 'INIT_RESP': InitResponseHandler(), 'MOVE_REQ': MoveRequest(connection),'MOVE_RESP':0,'END_REQ': EndRequest(connection)}

        while True:
            if self.state==0:
                dictionary['INIT_REQ'].request()
            json_response = connection.recv(1024)
            response = json.loads(json_response)
            label = response['label']
            try:
                self.state=dictionary[label].handle(connection,response)
            except KeyError:
                continue
            if self.state == 1:
                dictionary['MOVE_RESP'] = GomokuMoveResponseHandler()
                init=GomokuInitRequest(connection)
                init.request()
                self.state=4
            elif self.state == 2:
                dictionary['MOVE_RESP'] = MoreLessMoveResponseHandler()
                init=MoreLessInitRequest(connection)
                init.request()
                self.state=5
            elif self.state == 3:
                dictionary['END_REQ'].request()
                break
            elif self.state == 4:
                dictionary['MOVE_RESP']=GomokuMoveResponseHandler()
            elif self.state == 5:
                dictionary['MOVE_RESP'] = MoreLessMoveResponseHandler()

    def _create_socket(self):
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def _bind_socket(self,address,port):
        server_address=(address,port)
        self.sock.bind(server_address)

if __name__=="__main__":
    host='localhost'
    port=42012
    data_size=1024
    server=EchoServer(host, port,data_size)
    server.state_machine()
