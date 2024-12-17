class Corr:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    @classmethod
    def fromObj(cls, c: any):
        x = c["x"]
        y = c["y"]
        return Corr(x, y)

    def __eq__(self, other):
        if not isinstance(other, Corr):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))