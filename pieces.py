import pygame
from Morztypes import Vector2, Vector3, can_be_used_as_vector
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


class SlidingMove:
    """
    Class for making sliding moves\n
    Has starting move and step
    """

    def __init__(self, start, step):
        self._start = start
        self._step = step

    @property
    def start(self) -> Vector2:
        """
        Start position of the sliding move
        """
        return self._start

    @start.setter
    def start(self, value) -> None:
        if not can_be_used_as_vector(value):
            raise ValueError("Start is a Vector2, so it can only be set to int, float, Vector2, Vector3, list, tuple and set")

        self._start = value

    @property
    def step(self) -> Vector2:
        """
        Step of the sliding move
        """
        return self._step

    @step.setter
    def step(self, value) -> None:
        if not can_be_used_as_vector(value):
            raise ValueError("Step is a Vector2, so it can only be set to int, float, Vector2, Vector3, list, tuple and set")

        self._step = value


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
        You can use self.jumping_moves to easily set moves that jump over other pieces\n
        :param position: Vector2 initial position of the piece on the board
        :param is_white: True if the piece is white, false if the piece is black
        """

        self.value = self.White if is_white else self.Black
        self.position = Vector2(position)
        self._jumping_moves = []
        self._sliding_moves = []
        self.allow_any_and_direct_click_in_one = True
        self.can_capture_allies = False
        self.can_capture_enemies = True
        self.name = ""

    @property
    def jumping_moves(self) -> list[Vector2]:
        """
        List of jumping move relative positions of the piece
        """
        return self._jumping_moves

    @jumping_moves.setter
    def jumping_moves(self, value) -> None:
        if not isinstance(value, list):
            raise ValueError("Jumping moves is a list of Vector2 positions, so it can only be set to a list")

        all_values_are_vector2 = True
        for index, value_vector2 in enumerate(value):
            all_values_are_vector2 = all_values_are_vector2 and isinstance(value_vector2, Vector2)
            if not all_values_are_vector2:
                raise TypeError("Jumping moves is a list of Vector2 positions, but element " + str(index) + " in new list is not a Vector2")

        self._jumping_moves = value.copy()

    @property
    def sliding_moves(self) -> list[SlidingMove]:
        """
        List of SlidingMove's
        """
        return self._sliding_moves

    @sliding_moves.setter
    def sliding_moves(self, value) -> None:
        if not isinstance(value, list):
            raise ValueError("Sliding moves is a list of SlidingMove's, so it can only be set to a list")

        all_values_are_slidingmoves = True
        for index, value_slidingmove in enumerate(value):
            all_values_are_slidingmoves = all_values_are_slidingmoves and isinstance(value_slidingmove, SlidingMove)
            if not all_values_are_slidingmoves:
                raise TypeError("Sliding moves is a list of SlidingMove's, but element " + str(index) + " in new list is not a SlidingMove")

        self._sliding_moves = value.copy()

    @property
    def is_white(self) -> bool:
        """
        Shorthand for self.value // self.White == 1\n
        :return: True if the piece is white, false if the piece is black
        """

        return self.value // self.White == 1

    @property
    def forward(self) -> Vector2:
        """
        Forward direction of the piece, (0, -1) for white and (0, 1) for black
        """
        return Vector2(0, -1) if self.is_white else Vector2(0, 1)

    @property
    def backward(self) -> Vector2:
        """
        Backward direction of the piece, (0, 1) for white and (0, -1) for black
        """
        return Vector2(0, 1) if self.is_white else Vector2(0, -1)

    def get_moves_bitmap(self, board_size, black_pieces_bitmap, white_pieces_bitmap, black_pieces, white_pieces) -> int:
        """
        Bitmap starts from top-left, and goes from left to right\n
        Be sure to override this method when creating a new piece\n
        If you intend on using this and a custom method, you can do something like:\n
        bitmap = super().get_moves_bitmap(board_size)\n
        Then do some custom stuff with the bitmap and return it\n
        :return: The bitmap of all legal moves this piece can do
        """

        bitmap = 0

        bitmap |= self.calculate_jumping_moves(board_size, black_pieces_bitmap, white_pieces_bitmap)

        for sliding_move in self.sliding_moves:
            bitmap |= self.calculate_sliding_move(board_size, black_pieces_bitmap, white_pieces_bitmap, sliding_move)

        return bitmap

    def calculate_jumping_move(self, board_size, black_pieces_bitmap, white_pieces_bitmap, move) -> int:
        """
        Function that calculates one jumping move and returns the bitmap of it\n
        :param board_size: Vector2 size of the board
        :param black_pieces_bitmap: Bitmap of all the black pieces
        :param white_pieces_bitmap: Bitmap of all the black pieces
        :param move: Vector2 relative position of the move
        :return: Bitmap with a single or no bits, corresponding to the position of the move on the board
        """

        bit = self.position_to_bit(self.position + move, board_size)

        ally_pieces_bitmap = white_pieces_bitmap if self.is_white else black_pieces_bitmap
        enemy_pieces_bitmap = white_pieces_bitmap if not self.is_white else black_pieces_bitmap

        if not self.can_capture_allies:
            bit &= ~ally_pieces_bitmap

        if not self.can_capture_enemies:
            bit &= ~enemy_pieces_bitmap

        return bit

    def calculate_jumping_moves(self, board_size, black_pieces_bitmap, white_pieces_bitmap, moves=None) -> int:
        """
        Function that calculates all jumping moves in the list and returns the bitmap of them
        :param board_size: Vector2 size of the board
        :param black_pieces_bitmap: Bitmap of all the black pieces
        :param white_pieces_bitmap: Bitmap of all the black pieces
        :param moves: List of Vector2 relative positions of the moves
        :return: Bitmap with bits, corresponding to the positions of the moves on the board
        """

        _moves = moves
        if moves is None:
            _moves = self.jumping_moves

        bitmap = 0

        for move in _moves:
            bitmap += self.calculate_jumping_move(board_size, black_pieces_bitmap, white_pieces_bitmap, move)

        return bitmap

    def calculate_sliding_move(self, board_size, black_pieces_bitmap, white_pieces_bitmap, sliding_move) -> int:
        """
        Function that calculates and returns bitmap of a sliding move this piece can do\n
        :param board_size: The Vector2 size of the board
        :param black_pieces_bitmap: Bitmap of all black pieces
        :param white_pieces_bitmap: Bitmap of all white pieces
        :param sliding_move: SlidingMove object of the sliding move
        :return: Bitmap of the sliding move
        """

        bitmap = 0

        move_position = self.position + sliding_move.start

        # Bitmap of all pieces, made by ORing bitmaps of black and white pieces
        # Not adding them, because if for some reason two pieces end up on the same square, everything will go terribly wrong
        all_pieces_bitmap = black_pieces_bitmap | white_pieces_bitmap

        # Variable, that will help determine if the cursor hit any piece, or just moved out of the board
        out_of_the_board = False

        cell_under_the_cursor = 0

        # While move is on empty cell
        while move_position.inside_of(board_size):
            # Move the cursor
            move_position += sliding_move.step

            # The bit of cell under the cursor, it is None if there is no cell under the cursor
            cell_under_the_cursor = self.position_to_bit(move_position, board_size)

            # Break out of the loop, if there is no cell under the cursor
            if cell_under_the_cursor is None:
                out_of_the_board = True
                break

            # If there is a piece under the cursor
            if all_pieces_bitmap & cell_under_the_cursor != 0:
                break

            # If there is a cell under the cursor
            # Add the place under the cursor to moves bitmap by ORing (again, not adding, it is safer and faster to OR them)
            bitmap |= cell_under_the_cursor

        # If the cursor hit a piece, instead of moving out of the board
        if not out_of_the_board:
            # Variable, that will help determine if the piece that got hit by the move is white
            hit_white_piece = self.position_in_bitmap(white_pieces_bitmap, move_position, board_size)

            # True if the piece hit is the same color, False if not
            piece_hit_is_ally = hit_white_piece == self.is_white

            # You can change self.can_capture_allies in __init__() function, it is False by default
            if piece_hit_is_ally and self.can_capture_allies:
                bitmap |= self.position_to_bit(move_position, board_size)

            # You can change self.can_capture_enemies in __init__() function, it is False by default
            if not piece_hit_is_ally and self.can_capture_enemies:
                bitmap |= self.position_to_bit(move_position, board_size)

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

        if not pos.inside_of(bsize):
            return 0

        return (1 << pos.x) << (pos.y * bsize.x)

    def bit_to_position(self, bit, board_size) -> Vector2:
        """
        :param bit: Bitmap with (preferably) one bit on it, corrseponding to a position
        :param board_size: The Vector2 size of the board
        :return: Vector2 position of first bit in bitmap, if bitmap has more than one bit active in it, will return the lowest one (most top, then most left)
        """

        position = Vector2(0, 0)

        for i in range(board_size.area):
            bit = (bitmap >> i) % 2

            if bit:
                position = Vector2(i % board_size.x, i // board_size.x)

                break

        return position

    def bitmap_to_positions(self, bitmap) -> list[Vector2]:
        """
        Use this to convert bitmaps (like from Piece.get_moes_bitmap()) to a list of positions on the board
        :param bitmap: A target bitmap, starts from top-left, and then goes like text - left-to-right and top-to-bottom
        :return: List of Vector2 positions that are on a bitmap
        """

        positions = []

        for i in range(self.board.size.area):
            bit = (bitmap >> i) % 2

            if bit:
                positions.append(Vector2(i % self.board.size.x, i // self.board.size.x))

        return positions

    def position_in_bitmap(self, bitmap, position, board_size) -> bool:
        """
        Shorthand for (bitmap >> position.x) >> (position.y * board_size.x) == 1\n
        :param board_size: The size of the board
        :param bitmap: The bitmap to take position from
        :param position: Vector2 position, from top-left
        :return: True if there is 1 in the bitmap in target position, False if not or the position is out of the board
        """

        if not position.inside_of(board_size):
            return False

        bit = (bitmap >> position.x) >> (position.y * board_size.x)
        return bit % 2 == 1

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

    def on_captured(self, source_piece, forced_capture=False) -> bool:
        """
        Function automatically called when the piece is captured by another piece\n
        If forced_capture is True, then the piece will get removed regardless of the return\n
        :param source_piece: The piece that tried to capture this piece
        :param forced_capture: True if the capture is forced. Generally True when the piece is getting captured back by a piece it's trying to capture
        :return: True to allow this piece to get removed. False to not remove the piece and remove the piece that tried to capture instead
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

        self.jumping_moves = [
            Vector2(1, -2),
            Vector2(2, -1),
            Vector2(2, 1),
            Vector2(1, 2),
            Vector2(-1, 2),
            Vector2(-2, 1),
            Vector2(-2, -1),
            Vector2(-1, -2)
        ]


class Rook(Piece):
    def __init__(self, position, is_white):
        super().__init__(position, is_white)

        self.self_register("Rook")

        self.sliding_moves = [
            SlidingMove(Vector2(), Vector2(0, -1)),
            SlidingMove(Vector2(), Vector2(1, 0)),
            SlidingMove(Vector2(), Vector2(0, 1)),
            SlidingMove(Vector2(), Vector2(-1, 0)),
        ]
