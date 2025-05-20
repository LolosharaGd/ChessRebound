from Morztypes import Vector2, Vector3


class Piece:
    White = 1 << 6
    Black = 1 << 7

    Knight = 1

    # Up to 64 pieces!

    def __init__(self, position, is_white):
        """
        Standard initialization function\n
        When creating a new piece, make sure to call super().__init__(position, is_white) first and then set it's self.value\n
        To properly set piece's self.value you need to:\n
        self.value += index of your piece's type\n
        You can use self.relative_moves to easily set moves that jump over other pieces\n
        TODO: Make creating custom piece type indexes easy

        :param position: Vector2 initial position of the piece on the board
        :param is_white: True if the piece is white, false if the piece is black
        """

        self.value = self.White if is_white else self.Black
        self.position = Vector2(position)
        self.relative_moves = []

    @property
    def is_white(self) -> bool:
        """
        Shorthand for self.value // self.White == 1\n
        :return: True if the piece is white, false if the piece is black
        """

        return self.value // self.White == 1

    def get_moves_raw(self, board_size) -> int:
        """
        "Raw" means other pieces, checks, pins and everything else is ignored\n
        Bitmap starts from top-left, and goes from left to right\n
        Be sure to override this method when creating a new piece\n
        If you intend on using this and a custom method, you can do something like:\n
        bitmap = super().get_moves_raw(board_size)\n
        Then do some custom stuff with the bitmap and return it\n
        :return: The bitmap of all raw possible moves this piece can do
        """

        bitmap = 0

        for move in self.relative_moves:
            bitmap += self.position_to_bit(self.position + move, board_size)

        return bitmap

    def position_to_bit(self, position, board_size) -> int:
        """
        If the position is outside the board, returns 0\n
        Shorthand for (1 << position.x) << (position.y * board_size.x)

        :param position: Vector2 target position
        :param board_size: Vector2 size of the board
        :return: Integer with a single bit, corresponding to a place on bitmap
        """

        pos = Vector2(position)
        bsize = Vector2(board_size)

        if pos.x < 0 or pos.x >= bsize.x:
            return 0

        if pos.y < 0 or pos.y >= bsize.y:
            return 0

        return (1 << pos.x) << (pos.y * bsize.x)

    def self_bit_position(self, board_size) -> int:
        """
        Shorthand for piece.position_to_bit(piece.position, board_size)\n
        :return: Bitmap with 1 bit that corresponds to this piece's position
        """

        return self.position_to_bit(self.position, board_size)


class Knight(Piece):
    def __init__(self, position, is_white):
        super().__init__(position, is_white)

        self.value += self.Knight

        self.relative_moves = [
            Vector2(1, -2),
            Vector2(2, -1),
            Vector2(2, 1),
            Vector2(1, 2),
            Vector2(-1, 2),
            Vector2(-2, 1),
            Vector2(-2, -1),
            Vector2(-1, -2)
        ]
