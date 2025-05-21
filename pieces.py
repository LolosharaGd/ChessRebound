import pygame
from Morztypes import Vector2, Vector3
import global_vars

PieceTypes = {}
# Up to 64 pieces!
# Including base ones


def register_piece(name):
    """
    Registers the piece type, if it was not already registered\n
    Use PieceTypes[name of the piece type] to get the index of the piece type\n
    Will not do anything if the 64 piece types are registered\n
    :param name: Internal name of the piece type
    """

    if name not in PieceTypes and len(PieceTypes) < 64:
        PieceTypes[name] = len(PieceTypes)

        global_vars.TEXTURES[Piece.White + PieceTypes[name]] = pygame.image.load("Textures\\" + name + "White.png")
        global_vars.TEXTURES[Piece.Black + PieceTypes[name]] = pygame.image.load("Textures\\" + name + "Black.png")


class Piece:
    """
    Type that every piece stems from\n
    You can read in the documentation (README.md) how to create a new piece
    """

    White = 1 << 6
    Black = 1 << 7

    def __init__(self, position, is_white):
        """
        Standard initialization function\n
        When creating a new piece, make sure to call super().__init__(position, is_white) first and then set it's self.value\n
        To properly set piece's self.value you need to:\n
        self.self_register(name of the piece)\n
        This will create new piece type in PieceTypes, set this piece's self.value and self.name\n
        You can use self.relative_moves to easily set moves that jump over other pieces\n
        :param position: Vector2 initial position of the piece on the board
        :param is_white: True if the piece is white, false if the piece is black
        """

        self.value = self.White if is_white else self.Black
        self.position = Vector2(position)
        self.relative_moves = []
        self.allow_any_and_direct_click_in_one = True
        self.can_capture_allies = False
        self.can_capture_enemies = True
        self.name = ""

    @property
    def is_white(self) -> bool:
        """
        Shorthand for self.value // self.White == 1\n
        :return: True if the piece is white, false if the piece is black
        """

        return self.value // self.White == 1

    def get_moves_bitmap(self, board_size, black_pieces_bitmap, white_pieces_bitmap) -> int:
        """
        Bitmap starts from top-left, and goes from left to right\n
        Be sure to override this method when creating a new piece\n
        If you intend on using this and a custom method, you can do something like:\n
        bitmap = super().get_moves_bitmap(board_size)\n
        Then do some custom stuff with the bitmap and return it\n
        :return: The bitmap of all raw possible moves this piece can do
        """

        bitmap = 0

        for move in self.relative_moves:
            bitmap += self.position_to_bit(self.position + move, board_size)

        ally_pieces_bitmap = white_pieces_bitmap if self.is_white else black_pieces_bitmap
        enemy_pieces_bitmap = white_pieces_bitmap if not self.is_white else black_pieces_bitmap

        if not self.can_capture_allies:
            bitmap &= ~ally_pieces_bitmap

        if not self.can_capture_enemies:
            bitmap &= ~enemy_pieces_bitmap

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

    def on_click(self, position, on_board_position, button):
        """
        Function automatically called when click has happened somewhere on the screen\n
        This function is not called when the piece is clicked if self.allow_any_and_direct_click_in_one is False
        :param on_board_position: Position of the click on the board in cells
        :param position: Position of the click on the screen in pixels
        :param button: Button index that was pressed. 1, 2 and 3 for left, middle and right respectively
        """

        pass

    def clicked(self, button):
        """
        Function automatically called when the piece is clicked
        :param button: Button index that was pressed. 1, 2 and 3 for left, middle and right respectively
        """

        pass

    def on_click_release(self, position, on_board_position, button):
        """
        Function automatically called when click is released somewhere on the screen\n
        This function is not called when the piece is released if self.allow_any_and_direct_click_in_one is False\n
        :param on_board_position: Position of the click on the board in cells
        :param position: Position of the click on the screen in pixels
        :param button: Button index that was pressed. 1, 2 and 3 for left, middle and right respectively
        """

        pass

    def click_released(self, button):
        """
        Function automatically called when the piece is released
        :param button: Button index that was pressed. 1, 2 and 3 for left, middle and right respectively
        """

        pass

    def on_captured(self, source_piece, forced_capture) -> bool:
        """
        Function automatically called when the piece is captured by another piece\n
        :param source_piece: The piece that tried to capture this piece
        :param forced_capture: True if the capture is forced. Can be used if the piece is destroying the piece trying to capture it
        :return: True to allow this piece to get removed. False to not remove the piece, recommended to call another piece's Piece.on_captured(self, True) so two pieces do not end up on one spot
        """

        return True or forced_capture

    def self_register(self, name):
        self.name = name
        register_piece(self.name)
        self.value += PieceTypes[self.name]


class Knight(Piece):
    def __init__(self, position, is_white):
        super().__init__(position, is_white)

        self.self_register("Knight")

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
