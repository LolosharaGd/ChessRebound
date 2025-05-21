from Morztypes import Vector2, Vector3
from pieces import Piece, Knight, PieceTypes
from custom_pieces import *
# Sorry, I have to do the "from X import *" thing, because I don't know what will actually be in there and I don't want to make creating a new piece harder than it already is


class Board:
    def __init__(self, size):
        self.size = size
        self.pieces = []

    @property
    def white_pieces(self) -> list[Piece]:
        """
        List of all white pieces
        """

        result = []

        for piece in self.pieces:
            if piece.is_white:
                result.append(piece)

        return result

    @property
    def black_pieces(self) -> list[Piece]:
        """
        List of all black pieces
        """

        result = []

        for piece in self.pieces:
            if not piece.is_white:
                result.append(piece)

        return result

    @property
    def all_pieces_bitmap(self) -> int:
        """
        Bitmap of all pieces
        """

        bitmap = 0

        for piece in self.pieces:
            bit = piece.self_bit_position(self.size)

            bitmap |= bit

        return bitmap

    @property
    def white_pieces_bitmap(self) -> int:
        """
        Bitmap of all white pieces
        """

        bitmap = 0

        for piece in self.white_pieces:
            bit = piece.self_bit_position(self.size)

            bitmap |= bit

        return bitmap

    @property
    def black_pieces_bitmap(self) -> int:
        """
        Bitmap of all black pieces
        """

        bitmap = 0

        for piece in self.black_pieces:
            bit = piece.self_bit_position(self.size)

            bitmap |= bit

        return bitmap
