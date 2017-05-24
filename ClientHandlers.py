from AbstractHandler import AbstractHandler
from Message import Message
import json
import logging


class InitRequestHandler(AbstractHandler):
    def handle(self,sock,request):
        str_message=request['message']
        print(str_message)
        str_response=input()
        while len(str_response)==0:
            str_response = input()
        response=Message('INIT_RESP',str_response)
        logging.info('Sent INIT_RESP.')
        sock.send(str.encode(json.dumps(response.__dict__)))


class MoveRequestHandler(AbstractHandler):
    def handle(self,sock,request):
        str_message=request['message']
        print(str_message)
        str_response=input()
        while len(str_response)==0:
            str_response = input()
        response=Message('MOVE_RESP',str_response)
        logging.info('Sent MOVE_RESP.')
        sock.send(str.encode(json.dumps(response.__dict__)))


class EndRequestHandler(AbstractHandler):
    def handle(self, sock,request):
        str_message = request['message']
        print(str_message)
        logging.info('Disconnected successfully.')
        sock.close()
        exit()
