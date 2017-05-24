import abc


class AbstractValidator(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def validate(self):
        """validate the input"""
