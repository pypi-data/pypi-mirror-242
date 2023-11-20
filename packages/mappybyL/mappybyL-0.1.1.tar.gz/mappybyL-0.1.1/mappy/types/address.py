from mappy.error import InvalidTypeError

class Address:
    def __init__(self, address):
        if not isinstance(address, str):
            raise InvalidTypeError(address, "'경기도 화성시 남양읍 남양성지로 147'")
        self.address = address

    def __str__(self):
        return self.address