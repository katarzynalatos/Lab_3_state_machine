import abc


class AbstractHandler(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def handle(self,Client,message):
        """Handle messages"""


