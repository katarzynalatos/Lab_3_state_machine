from enum import Enum


class Label(Enum):
    INIT_REQ=1
    INIT_RESP=2
    MOVE_REQ=3
    MOVE_RESP=4
    END_REQ=5
    END_RESP=6


class Message:
    def __init__(self, label, message):
        self.label=label
        self.message=message
