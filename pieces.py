from Morztypes import Vector2, Vector3


class Piece:
    White = 1 << 6
    Black = 1 << 7

    Knight = 1

    def __init__(self, position):
        self.value = self.White + self.Knight
        self.position = Vector2(position)

    @property
    def is_white(self) -> bool:
        return self.value // self.White == 1


class Knight(Piece):
    def __init__(self, position, is_white):
        super().__init__(position)

        self.value = self.Knight
        self.value += self.White if is_white else self.Black
