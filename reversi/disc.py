class Disc:
    _instance_count = 0

    def __init__(self, name, symbol, code=None):
        cls = type(self)
        self.code = cls._instance_count if code is None else code
        self.name = name
        self.symbol = symbol
        cls._instance_count += 1 if cls._instance_count < 1000 else 0

    def __int__(self):
        return self.code

    def __repr__(self):
        return f'<Disc {self.name!r}, {self.symbol!r}>'
