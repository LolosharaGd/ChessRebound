from Morztypes import Vector2, Vector3
from pieces import Piece, Knight, PieceTypes
from custom_pieces import *
# Sorry, I have to do the "from X import *" thing, because I don't know what will actually be in there and I don't want to make creating a new piece harder than it already is


class Board:
    def __init__(self, size):
        self.size = size
        self.pieces = []

    def get_piece_at(self, position) -> Piece:
        """
        Funtiction that returns the piece at a given position\n
        Will return None if there are no pieces in given position\n
        :param position: Vector2 position at which to get the piece
        :return: Piece object if there is a piece here, None if there is no pieces here
        """

        result_piece = None

        there_is_a_piece = ((self.all_pieces_bitmap >> Vector2(position).x) >> (Vector2(position).y * self.size.x)) % 2 == 1

        if there_is_a_piece:
            for piece in self.pieces:
                if piece.position == Vector2(position):
                    result_piece = piece

                    break

        return result_piece

    @property
    def white_moves_bitmap(self):
        """
        All moves white can do, checks are not accounted for
        """

        bitmap = 0

        for piece in self.pieces:
            if piece.is_white:
                bitmap |= piece.get_moves_bitmap(self.size, self.black_pieces_bitmap, self.white_pieces_bitmap, self.black_pieces, self.white_pieces)

        return bitmap

    @property
    def black_moves_bitmap(self):
        """
        All moves black ca ndo, checks are not accounted for
        """

        bitmap = 0

        for piece in self.pieces:
            if not piece.is_white:
                bitmap |= piece.get_moves_bitmap(self.size, self.black_pieces_bitmap, self.white_pieces_bitmap, self.black_pieces, self.white_pieces)

        return bitmap

    def get_piece_type(self, name):
        """
        List of all pieces of the given type
        :param name: Internal name of the piece type
        """

        result = []

        for piece in self.pieces:
            if piece.name == name:
                result.append(piece)

        return result

    def get_piece_type_moves_bitmap(self, name, white=None):
        """
        :param white: True to get only moves of white pieces of this type, False to only get the moves of black pieces of that type. Leave at None to get both
        :param name: Internal name of the piece type
        :return: Bitmap of all moves this type of piece can do
        """

        bitmap = 0

        for piece in self.get_piece_type(name):
            if piece.is_white is white or white is None:
                bitmap |= piece.get_moves_bitmap(self.size, self.black_pieces_bitmap, self.white_pieces_bitmap, self.black_pieces, self.white_pieces)

        return bitmap

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
    def royal_pieces(self) -> list[Piece]:
        """
        List of all royal pieces (pieces that can be put in check)
        """

        result = []

        for piece in self.pieces:
            if piece.royal:
                result.append(piece)

        return result

    @property
    def non_royal_pieces(self) -> list[Piece]:
        """
        List of all non-royal pieces (pieces that can't be put in check)
        """

        result = []

        for piece in self.pieces:
            if not piece.royal:
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

    @property
    def royal_pieces_bitmap(self) -> int:
        """
        Bitmap of all royal pieces
        """

        bitmap = 0

        for piece in self.royal_pieces:
            bit = piece.self_bit_position(self.size)

            bitmap |= bit

        return bitmap

    @property
    def non_royal_pieces_bitmap(self) -> int:
        """
        Bitmap of all non-royal pieces
        """

        bitmap = 0

        for piece in self.non_royal_pieces:
            bit = piece.self_bit_position(self.size)

            bitmap |= bit

        return bitmap
