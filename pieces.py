import pygame
from Morztypes import Vector2, Vector3, can_be_used_as_vector
import global_vars
import math

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
        self.royal = False
        self.transparent = False
        self.attacked = False

        self.post_modifies_moves = False

        # Used after on_other_piece_moved, on_piece_moved, on_captured
        self.pieces_to_summon = []
        self.pieces_to_capture = []

        self.invisible = False

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

        all_pieces = black_pieces + white_pieces

        transparent_pieces = 0
        for piece in all_pieces:
            if piece.transparent:
                transparent_pieces |= piece.self_bit_position(board_size)

        for sliding_move in self.sliding_moves:
            bitmap |= self.calculate_sliding_move(board_size, black_pieces_bitmap, white_pieces_bitmap, sliding_move, 0, transparent_pieces)

        return bitmap

    def post_modify_moves(self, board_size, black_pieces_bitmap, white_pieces_bitmap, black_pieces, white_pieces, moves_bitmap) -> int:
        """
        Function that is called after get_moves_bitmap(), by default just echoes bitmap put into it\n
        But you can modify this function, because it as given bitmap of moves that includes only legal moves\n
        :param board_size: Vector2 size of the board
        :param black_pieces_bitmap: Bitmap of all black pieces
        :param white_pieces_bitmap: Bitmap of all white pieces
        :param black_pieces: List of all black Piece object
        :param white_pieces: List of all white Piece objects
        :param moves_bitmap: Bitmap of moves that was returned by get_moves_bitmap(), modified to only have legal moves
        :return: Bitmap of new moves
        """

        return moves_bitmap

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

    def calculate_sliding_move(self, board_size, black_pieces_bitmap, white_pieces_bitmap, sliding_move, extra_stoppers, transparent_pieces) -> int:
        """
        Function that calculates and returns bitmap of a sliding move this piece can do\n
        :param transparent_pieces: Bitmap of pieces that are transparent to sliding moves, meaning they do not stop them
        :param extra_stoppers: Bitmap of extra stoppers, like pieces are defalut stoppers
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
            if ((all_pieces_bitmap | extra_stoppers) & ~transparent_pieces) & cell_under_the_cursor != 0:
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
            _bit = (bit >> i) % 2

            if _bit:
                position = Vector2(i % board_size.x, i // board_size.x)

                break

        return position

    def position_in_bitmap(self, bitmap, position, board_size) -> bool:
        """
        Shorthand for (bitmap >> position.x) >> (position.y * board_size.x) % 2 == 1\n
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

    def on_captured(self, source_piece, black_pieces, white_pieces, forced_capture=False) -> bool:
        """
        Function automatically called when the piece is captured by another piece\n
        If forced_capture is True, then the piece will get removed regardless of the return\n
        :param white_pieces: List of all white pieces
        :param black_pieces: List of all black pieces
        :param source_piece: The piece that tried to capture this piece
        :param forced_capture: True if the capture is forced. Generally True when the piece is getting captured back by a piece it's trying to capture
        :return: True to allow this piece to get removed. False to not remove the piece and remove the piece that tried to capture instead
        """

        return True or forced_capture

    def on_moved(self, board_size, new_position, captured_piece, black_pieces, white_pieces):
        """
        Function automatically called when a piece is moved\n
        Keep in mind that this function is also called when the piece is fake-moved when checking for legal moves\n
        This function is called before moving the piece or capturing another piece\n
        :param board_size: Vector2 size of the board
        :param new_position: Vector2 new position of the piece
        :param black_pieces: List of all black pieces
        :param white_pieces: List of all white pieces
        :param captured_piece: Piece that is going to be captured by this move, None if no piece is going to be captured
        """

        pass

    def on_other_piece_moved(self, board_size, new_position, piece, captured_piece, black_pieces, white_pieces):
        """
        Function automatically called before other piece is moved\n
        Keep in mind that this function is also called when the piece is fake-moved when checking for legal moves\n
        To get the old position of the piece, just use piece.position, because this function is called BEFORE the move a removing of the captured piece\n
        :param board_size: Vector2 size of the board
        :param new_position: New position of the piece
        :param piece: Piece object of the piece being moved
        :param captured_piece: Piece that is going to be captured by this move, None if no piece is going to be captured
        :param black_pieces: List of all black pieces
        :param white_pieces: List of all white pieces
        """

        pass

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

    def on_moved(self, board_size, new_position, captured_piece, black_pieces, white_pieces):
        ally_pieces = white_pieces if self.is_white else black_pieces

        for ally in ally_pieces:
            if ally.name == "King":
                if self.position.x == 7:
                    ally.kingside_castle_allowed = False
                elif self.position.x == 0:
                    ally.queenside_castle_allowed = False


class Bishop(Piece):
    def __init__(self, position, is_white):
        super().__init__(position, is_white)

        self.self_register("Bishop")

        self.sliding_moves = [
            SlidingMove(Vector2(), Vector2(1, -1)),
            SlidingMove(Vector2(), Vector2(1, 1)),
            SlidingMove(Vector2(), Vector2(-1, 1)),
            SlidingMove(Vector2(), Vector2(-1, -1)),
        ]


class Queen(Piece):
    def __init__(self, position, is_white):
        super().__init__(position, is_white)

        self.self_register("Queen")

        self.sliding_moves = [
            SlidingMove(Vector2(), Vector2(0, -1)),
            SlidingMove(Vector2(), Vector2(1, 0)),
            SlidingMove(Vector2(), Vector2(0, 1)),
            SlidingMove(Vector2(), Vector2(-1, 0)),
            SlidingMove(Vector2(), Vector2(1, -1)),
            SlidingMove(Vector2(), Vector2(1, 1)),
            SlidingMove(Vector2(), Vector2(-1, 1)),
            SlidingMove(Vector2(), Vector2(-1, -1)),
        ]


class King(Piece):
    def __init__(self, position, is_white):
        super().__init__(position, is_white)

        self.self_register("King")

        self.jumping_moves = [
            Vector2(0, -1),
            Vector2(1, -1),
            Vector2(1, 0),
            Vector2(1, 1),
            Vector2(0, 1),
            Vector2(-1, 1),
            Vector2(-1, 0),
            Vector2(-1, -1)
        ]

        self.royal = True

        self.kingside_castle_allowed = True
        self.queenside_castle_allowed = True

        self.post_modifies_moves = True

    def post_modify_moves(self, board_size, black_pieces_bitmap, white_pieces_bitmap, black_pieces, white_pieces, moves_bitmap) -> int:
        bitmap = moves_bitmap

        if not self.attacked:
            all_pieces_bitmap = black_pieces_bitmap | white_pieces_bitmap
            enemy_pieces_bitmap = black_pieces_bitmap if self.is_white else white_pieces_bitmap
            ally_pieces_bitmap = black_pieces_bitmap if not self.is_white else white_pieces_bitmap

            near_kingside_pos = self.position_in_bitmap(all_pieces_bitmap, self.position + Vector2(1, 0), board_size)
            far_kingside_pos = self.position_in_bitmap(all_pieces_bitmap, self.position + Vector2(2, 0), board_size)
            near_queenside_pos = self.position_in_bitmap(all_pieces_bitmap, self.position - Vector2(1, 0), board_size)
            far_queenside_pos = self.position_in_bitmap(all_pieces_bitmap, self.position - Vector2(2, 0), board_size)
            farthest_queenside_pos = self.position_in_bitmap(all_pieces_bitmap, self.position - Vector2(3, 0), board_size)

            check_on_kingside = not self.position_in_bitmap(moves_bitmap, self.position + Vector2(1, 0), board_size)
            check_on_queenside = not self.position_in_bitmap(moves_bitmap, self.position - Vector2(1, 0), board_size)

            if self.kingside_castle_allowed:
                if not (near_kingside_pos or far_kingside_pos or check_on_kingside):
                    bitmap |= self.position_to_bit(self.position + Vector2(2, 0), board_size)

            if self.queenside_castle_allowed:
                if not (near_queenside_pos or far_queenside_pos or farthest_queenside_pos or check_on_queenside):
                    bitmap |= self.position_to_bit(self.position - Vector2(2, 0), board_size)

        return bitmap

    def on_moved(self, board_size, new_position, captured_piece, black_pieces, white_pieces):
        self.kingside_castle_allowed = False
        self.queenside_castle_allowed = False

        ally_pieces = white_pieces if self.is_white else black_pieces

        if self.position.x == 4 and new_position.x == 6:  # Kingside castle
            for ally in ally_pieces:
                if ally.name == "Rook":
                    if ally.position.x == 7:
                        ally.position.x = 5

                        break

        if self.position.x == 4 and new_position.x == 2:  # Kingside castle
            for ally in ally_pieces:
                if ally.name == "Rook":
                    if ally.position.x == 0:
                        ally.position.x = 3

                        break


class Pawn(Piece):
    def __init__(self, position, is_white):
        super().__init__(position, is_white)

        self.self_register("Pawn")

    def get_moves_bitmap(self, board_size, black_pieces_bitmap, white_pieces_bitmap, black_pieces, white_pieces) -> int:
        bitmap = 0

        all_pieces_bitmap = black_pieces_bitmap | white_pieces_bitmap
        enemy_pieces_bitmap = black_pieces_bitmap if self.is_white else white_pieces_bitmap
        ally_pieces_bitmap = black_pieces_bitmap if not self.is_white else white_pieces_bitmap

        # If the space above is free
        if self.position_to_bit(self.position + self.forward, board_size) & all_pieces_bitmap == 0:
            bitmap |= self.position_to_bit(self.position + self.forward, board_size)

            # If the space above it is free AND the pawn is on 2nd or 7th rank
            if self.position_to_bit(self.position + self.forward * 2, board_size) & all_pieces_bitmap == 0 and self.position.y in [1, 6]:
                bitmap |= self.position_to_bit(self.position + self.forward * 2, board_size)

        for move_position in [Vector2(1, 0), Vector2(-1, 0)]:
            move_bit = self.position_to_bit(self.position + self.forward + move_position, board_size)

            enemy_on_move = move_bit & enemy_pieces_bitmap
            ally_on_move = move_bit & ally_pieces_bitmap

            if (enemy_on_move and self.can_capture_enemies) or (ally_on_move and self.can_capture_allies):
                bitmap |= move_bit

        return bitmap

    def on_moved(self, board_size, new_position, captured_piece, black_pieces, white_pieces):
        if math.fabs((new_position - self.position).y) == 2:
            self.pieces_to_summon.append(EnPassant(self.position + self.forward, self.is_white))


class EnPassant(Piece):
    def __init__(self, position, is_white):
        super().__init__(position, is_white)

        self.self_register("EnPassant")

        self.transparent = True
        self.invisible = True

    def get_moves_bitmap(self, board_size, black_pieces_bitmap, white_pieces_bitmap, black_pieces, white_pieces) -> int:
        # Just return 0 so it doesn't waste time
        return 0

    def on_captured(self, source_piece, black_pieces, white_pieces, forced_capture=False) -> bool:
        ally_pieces = white_pieces if self.is_white else black_pieces

        if source_piece.name == "Pawn":
            corresponding_pawn = None

            for piece in ally_pieces:
                if piece.position == self.position + self.forward:
                    corresponding_pawn = piece

                    break

            if corresponding_pawn is not None:
                self.pieces_to_capture.append(corresponding_pawn)

        return True

    def on_other_piece_moved(self, board_size, new_position, piece, captured_piece, black_pieces, white_pieces):
        if captured_piece != self and not (new_position == self.position + self.forward and piece.name == "Pawn" and piece.is_white == self.is_white):
            self.pieces_to_capture.append(self)
