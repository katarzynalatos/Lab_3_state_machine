import logging


class Player:
    def __init__(self, sign=0, nr=0):
        logging.info("Player no "+str(nr)+" had sign: " +str(sign)+".")
        #player nr =1
        #computer nr=0
        self.sign=sign
        #value -1 means X
        #value 1 means O
        self.nr=nr

