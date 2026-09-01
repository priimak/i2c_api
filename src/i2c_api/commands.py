class Command:
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"


class S(Command):
    pass


class Address(Command):
    def __init__(self, address: int):
        self.address = address

    def __repr__(self) -> str:
        if self.address == -1:
            return f"{self.__class__.__name__}(auto)"
        else:
            return f"{self.__class__.__name__}(0x{self.address:02X})"


class Address10(Command):
    def __init__(self, address: int):
        self.address = address

    def __repr__(self) -> str:
        if self.address == -1:
            return f"{self.__class__.__name__}(auto)"
        else:
            return f"{self.__class__.__name__}(0x{self.address:02X})"


class R(Command):
    pass


class W(Command):
    pass


class Data(Command):
    def __init__(self, data: int):
        self.data = data

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(0x{self.data:02X})"


class Read(Command):
    def __init__(self, num_bytes: int):
        self.num_bytes = num_bytes

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.num_bytes})"


class Sr(Command):
    pass


class P(Command):
    pass
