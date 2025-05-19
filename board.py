from Morztypes import Vector2, Vector3
from pieces import Piece, Knight


class Board:
    def __init__(self, size):
        self.size = size
        self.pieces = []

    @property
    def white_pieces(self) -> list[Piece]:
        result = []

        for piece in self.pieces:
            if piece.is_white:
                result.append(piece)

        return result

    @property
    def black_pieces(self) -> list[Piece]:
        result = []

        for piece in self.pieces:
            if not piece.is_white:
                result.append(piece)

        return result
