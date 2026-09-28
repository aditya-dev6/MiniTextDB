class AlreadyExistException(Exception):
    pass


class DoesNotExistException(Exception):
    pass


class EmptyException(Exception):
    pass


class Success:
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
