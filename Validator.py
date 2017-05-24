from AbstractValidator import AbstractValidator
import Exceptions


class Validator(AbstractValidator):
    def __init__(self, to_validate):
        super(Validator, self).__init__()
        self._to_validate = to_validate

    def validate_name(self):
        if self._is_not_a_string(self._to_validate):
            raise Exceptions.NotAString
        else:
            return True

    def validate_number(self):
        if self._is_not_int_number(self._to_validate):
            raise Exceptions.NotAIntNumber
        else:
            return True

    @staticmethod
    def _is_not_a_string(string):
        if isinstance(string, str):
            return False
        else:
            return True

    @staticmethod
    def _is_not_int_number(integer):
        if isinstance(integer, int):
            return False
        else:
            return True
