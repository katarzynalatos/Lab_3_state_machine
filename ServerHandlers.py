from AbstractHandler import AbstractHandler
from AbstratRequest import AbstractRequest
from GomokuStarter import GomokuStarter
from MoreLess import MoreLess
from Player import Player
from Board import Board
from random import randint
from Message import Message
import json
import logging


class InitResponseHandler(AbstractHandler):
    def __init__(self):
        pass

    def handle(self,Client,response):
        str_message=response['message']
        if str_message==str(1):
            logging.info("Player chose Gomoku game.")
            global new_game
            new_game=GomokuStarter()
            return 1
        elif str_message==str(2):
            logging.info("Player chose More Less game.")
            global new_game2
            new_game2 = MoreLess()
            return 2
        elif str_message==str(3) or str_message == "END":
            logging.info("Player ended game game.")
            return 3
        else:
            logging.info("Player typed incorrect data.")
            return 0


class GomokuInitRequest():
    def __init__(self,Client):
        self.client=Client

    def request(self):
        request = Message('MOVE_REQ',"\nG O M O K U\nWhat is your name?")
        self.client.send(str.encode(json.dumps(request.__dict__)))


class MoreLessInitRequest(AbstractRequest):
    def __init__(self, Client):
        self.client = Client

    def request(self):
        request = Message('MOVE_REQ',"\nM O R E  L E S S\nWhat is your name?")
        self.client.send(str.encode(json.dumps(request.__dict__)))


class InitRequest(AbstractRequest):
    def __init__(self,Client):
        self.client=Client

    def request(self):
        request = Message('INIT_REQ','Connected successfully\n\n 1 Play GOMOKU\n 2 Play MORE-LESS\n 3 Exit\n\n\nType "END" to exit in any time' )
        self.client.send(str.encode(json.dumps(request.__dict__)))


class GomokuMoveResponseHandler(AbstractHandler):
    def __init__(self):
        pass

    def handle(self, Client,response):
        str_message = response['message']
        if str_message == "END":
            return 3
        if new_game.done==0:
            if new_game.name == "":
                logging.info("Player typed name")
                new_game.name = str_message
                response = Message('MOVE_REQ',
                                   '{} what board size do you prefer? Choose 3,4,5,6,7,8,9 or 10'.format(new_game.name))
                Client.send(str.encode(json.dumps(response.__dict__)))
                return 4
            elif new_game.size == 0:
                try:
                    int(str_message)
                except ValueError:
                    logging.info("Player typed incorrect board size")
                    response = Message('MOVE_REQ',
                                       'This size is incorrect.\n{} what board size do you prefer? Choose 3,4,5,6,7,8,9 or 10'.format(
                                           new_game.name))
                    Client.send(str.encode(json.dumps(response.__dict__)))
                    return 4
                if int(str_message) <=2 or int(str_message) >= 11:
                    logging.info("Player typed incorrect board size")
                    response = Message('MOVE_REQ',
                                       'This size is incorrect.\n{} what board size do you prefer? Choose 3,4,5,6,7,8,9 or 10'.format(
                                           new_game.name))
                    Client.send(str.encode(json.dumps(response.__dict__)))
                    return 4
                else:
                    new_game.size=int(str_message)
                    logging.info("Player typed board size.")
                    response = Message('MOVE_REQ','Would you like "O" or "X"? "O" type 1, "X" type -1')
                    Client.send(str.encode(json.dumps(response.__dict__)))
                    return 4
            elif new_game.sign == 0:
                try:
                    int(str_message)
                except ValueError:
                    logging.info("Player typed incorrect sign")
                    response = Message('MOVE_REQ',
                                       'This sign is incorrect.\n{} choose again. "O" type 1, "X" type -1'.format(
                                           new_game.name))
                    Client.send(str.encode(json.dumps(response.__dict__)))
                    return 4
                if int(str_message)!=-1 and int(str_message)!=1:
                    logging.info("Player typed incorrect sign")
                    response = Message('MOVE_REQ',
                                       'This sign is incorrect.\n{} choose again. "O" type 1, "X" type -1'.format(
                                           new_game.name))
                    Client.send(str.encode(json.dumps(response.__dict__)))
                    return 4
                else:
                    new_game.sign=int(str_message)
                    logging.info("Player typed sign.")
                    new_game.player1=Player(new_game.sign, 1)
                    sign=int(new_game.sign)
                    sign=-sign
                    new_game.player0=Player(sign,0)
                    new_game.board=Board(new_game.size)
                    new_game.done=1
                    logging.info("Player played.")
                    response = Message('MOVE_REQ',new_game.board.write_board()+"\nIt's your turn now!\nGive row (X) position of your choice")
                    Client.send(str.encode(json.dumps(response.__dict__)))
                    return 4
        else:
             if new_game.row_position==0:
                 try:
                     int(str_message)
                 except ValueError:
                     logging.info("Player typed incorrect row position")
                     response = Message('MOVE_REQ',
                                        'Incorrect position number. Give row (X) position of your choice from [1,{}]'.format(new_game.board.size))
                     Client.send(str.encode(json.dumps(response.__dict__)))
                     return 4
                 if int(str_message) < 1 or int(str_message) > new_game.size:
                     logging.info("Player typed incorrect row position")
                     response = Message('MOVE_REQ',
                                        'Incorrect position number. Give row (X) position of your choice from [1,{}]'.format(new_game.board.size))
                     Client.send(str.encode(json.dumps(response.__dict__)))
                     return 4
                 else:
                     new_game.row_position = int(str_message)
                     logging.info("Player typed position x.")
                     response = Message('MOVE_REQ','Give column (Y) position of your choice')
                     Client.send(str.encode(json.dumps(response.__dict__)))
                     return 4
             elif new_game.column_position==0:
                 try:
                     int(str_message)
                 except ValueError:
                     logging.info("Player typed incorrect column position")
                     response = Message('MOVE_REQ',
                                        'Incorrect position number. Give column (Y) position of your choice from [1,{}]'.format(new_game.board.size))
                     Client.send(str.encode(json.dumps(response.__dict__)))
                     return 4
                 if int(str_message) < 1 or int(str_message) > new_game.size:
                     logging.info("Player typed incorrect row position")
                     response = Message('MOVE_REQ',
                                        'Incorrect position number. Give column (Y) position of your choice from [1,{}]'.format(new_game.board.size))
                     Client.send(str.encode(json.dumps(response.__dict__)))
                     return 4
                 else:
                     new_game.column_position = int(str_message)
                     logging.info("Player typed position y.")
                     if new_game.board.set_position(new_game.row_position, new_game.column_position, new_game.player1.sign, Client):
                         new_game.player_number = 0
                         new_game.row_position = 0
                         new_game.column_position = 0
                     else:
                         response = Message('MOVE_REQ','You chose not empty position.\nGive row (X) position of your choice from [1,{}]'.format(
                                                new_game.board.size))
                         Client.send(str.encode(json.dumps(response.__dict__)))
                         new_game.row_position = 0
                         new_game.column_position = 0
                         return 4
                     if new_game.board.is_winner(Client, new_game.player0):
                         logging.info("Player won Gomoku game.")
                         message = Message('END_REQ', new_game.board.write_board()+"\nGood job, you won Gomoku game.\n\nSuccessfully disconnected.")
                         Client.send(str.encode(json.dumps(message.__dict__)))
                         return 3
                     """COMPUTER TURN"""
                     logging.info("Computer played.")
                     position_x = randint(1, new_game.board.size)
                     position_y = randint(1, new_game.board.size)
                     while not new_game.board.set_position(position_x, position_y, new_game.player0.sign, Client):
                         position_x = randint(1, new_game.board.size)
                         position_y = randint(1, new_game.board.size)
                     if new_game.board.is_winner(Client, new_game.player0):
                         logging.info("Computer won Gomoku game.")
                         message = Message('END_REQ', new_game.board.write_board()+"\nSorry, computer won Gomoku game.\n\nSuccessfully disconnected.")
                         Client.send(str.encode(json.dumps(message.__dict__)))
                         return 3
                     else:
                         logging.info("Player played.")
                         response = Message('MOVE_REQ',
                                            new_game.board.write_board() + "\nIt's your turn now!\nGive row (X) position of your choice")
                         Client.send(str.encode(json.dumps(response.__dict__)))
                         return 4


class MoreLessMoveResponseHandler(AbstractHandler):
    def __init__(self):
        pass

    def handle(self, Client,response):
        str_message = response['message']
        if str_message == "END":
            return 3
        if new_game2.name=="":
            logging.info("Player typed name")
            new_game2.name=str_message
            response = Message('MOVE_REQ','{} guess my value between 1 and 1000...'.format(new_game2.name))
        else:
            try:
                new_game2.value=int(str_message)
                if new_game2.value > new_game2.number:
                    response = Message('MOVE_REQ', '{} my value is LESS than {}. Guess value between 1 and 1000...'.format(
                        new_game2.name,new_game2.value))
                    logging.info("Player chose too big value: " + str(new_game2.value))
                elif new_game2.value < new_game2.number:
                    response = Message('MOVE_REQ', '{} my value is MORE than {}. Guess value between 1 and 1000...'.format(
                        new_game2.name, new_game2.value))
                    logging.info("Player chose too small value: " + str(new_game2.value))
                elif new_game2.value == new_game2.number:
                    logging.info("Player won More Less game. Value: " + str(new_game2.value))
                    message = Message('END_REQ', "Good job, my value was: "+str(new_game2.number)+"\n\nSuccessfully disconnected.")
                    Client.send(str.encode(json.dumps(message.__dict__)))
                    return 3
            except ValueError:
                response = Message('MOVE_REQ','Incorrect data. {} guess value between 1 and 1000'.format(new_game2.name))
                logging.info("Player typed incorrect data.")
        Client.send(str.encode(json.dumps(response.__dict__)))
        return 5


class MoveRequest(AbstractRequest):
    def __init__(self,Client):
        self.client=Client

    def request(self):
        message = Message(1,
                          'Connected successfully\n\n 1 Play GOMOKU\n 2 Play MORE-LESS\n 3 Exit\n\n\nType "END" to exit in any time')
        # print(json.dumps(message.__dict__))
        self.client.send(str.encode(json.dumps(message.__dict__)))


class EndResponseHandler(AbstractHandler):
    def __init__(self):
        pass

    def handle(self,Client,response):
        str_message = response['message']
        print(str_message)
        if str_message=="END":
            return 3
        return 6


class EndRequest(AbstractRequest):
    def __init__(self, Client):
        self.client = Client

    def request(self):
        logging.info("Player successfully disconnected.")
        logging.shutdown()
        message = Message('END_REQ','Successfully disconnected')
        self.client.send(str.encode(json.dumps(message.__dict__)))


