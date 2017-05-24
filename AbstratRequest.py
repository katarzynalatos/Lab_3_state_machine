import abc


class AbstractRequest(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def request(self):
        """make requests"""
