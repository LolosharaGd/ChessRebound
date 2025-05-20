import pygame
from Morztypes import Vector2, Vector3, can_be_used_as_vector
from board import Board
from pieces import Piece, Knight

pygame.init()


class Main:
    """
    Main game class, contains main game loop function "run()" and other global variables
    """

    def __init__(self, resolution=Vector2(1920, 1080), fps=120):
        self._window_resolution = resolution

        self._fps = fps

        self._display = pygame.display.set_mode(resolution.unwrap())

        self._clock = pygame.time.Clock()

        self._color_palette = [Vector3(243, 238, 234), Vector3(235, 227, 213), Vector3(176, 166, 149), Vector3(119, 107, 93)]

        self._background_color = self.color_palette[0]

        self.icon = pygame.image.load("Textures\\Icon.png")

        self._board_cell_size = Vector2(100, 100)
        self._white_cell_color = self.color_palette[1]
        self._black_cell_color = self.color_palette[2]
        self._board_position = Vector2(140, 140)

        self._board = Board(Vector2(8, 8))

        self._board_surface = pygame.Surface(self.total_board_size.unwrap()).convert_alpha()

        self.pieces_surface = pygame.Surface(self.total_board_size.unwrap()).convert_alpha()

        self.selected_piece = 0
        self.is_piece_selected = False

        self.selected_legal_moves_bitmap = 0

        self._on_board_indicators_alpha = 64
        self.on_board_indicators_colors = [
            [100, 200, 0, self.on_board_indicators_alpha],  # Allowed moves
            [150, 200, 0, self.on_board_indicators_alpha],  # Selected piece
        ]

        self._click_position = Vector2()

        self.textures = {
            Piece.White + Piece.Knight: pygame.image.load("Textures\\KnightWhite.png"),
            Piece.Black + Piece.Knight: pygame.image.load("Textures\\KnightBlack.png")
        }

    def run(self):
        """
        Main game loop function
        """

        pygame.display.set_icon(self.icon)
        pygame.display.set_caption("Chess Rebound")

        self.board.pieces.append(Knight(Vector2(2, 3), True))
        self.board.pieces.append(Knight(Vector2(3, 1), True))

        while True:
            self.display.fill(self.background_color.unwrap())
            self.board_surface.fill(self.background_color.unwrap())
            self.pieces_surface.fill((0, 0, 0, 0))

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.close_game()

                elif e.type == pygame.KEYDOWN:
                    if e.unicode == "":
                        self.close_game()

                elif e.type == pygame.MOUSEBUTTONDOWN:
                    mouse_position = Vector2(e.pos)

                    self.mouse_click(mouse_position, e.button)

                elif e.type == pygame.MOUSEBUTTONUP:
                    mouse_position = Vector2(e.pos)

                    self.mouse_release(mouse_position, e.button)

            # Draw the board
            for cell_x in range(self.board.size.x):
                for cell_y in range(self.board.size.y):
                    cell_position = self.board_cell_size * Vector2(cell_x, cell_y)
                    cell_rect = cell_position.unwrap() + self.board_cell_size.unwrap()

                    if (cell_x + cell_y) % 2 == 0:
                        # If the cell is white
                        pygame.draw.rect(self.board_surface, self.white_cell_color.unwrap(), cell_rect)
                    else:
                        # If the cell is black
                        pygame.draw.rect(self.board_surface, self.black_cell_color.unwrap(), cell_rect)

            # Draw selected cell
            selected_piece_position = self.board.pieces[self.selected_piece].position * self.board_cell_size
            if self.is_piece_selected:
                pygame.draw.rect(self.board_surface, self.on_board_indicators_colors[1], selected_piece_position.unwrap() + self.board_cell_size.unwrap())

            # Draw selected legal moves
            if self.is_piece_selected:
                for move_position in self.bitmap_to_positions(self.selected_legal_moves_bitmap):
                    pygame.draw.rect(self.board_surface, self.on_board_indicators_colors[0], (move_position * self.board_cell_size).unwrap() + self.board_cell_size.unwrap())

            # Draw the pieces
            for index, piece in enumerate(self.board.pieces):
                piece_position = piece.position * self.board_cell_size
                self.pieces_surface.blit(pygame.transform.scale(self.textures[piece.value], self.board_cell_size.unwrap()), piece_position.unwrap())

            # Blit the surfaces
            # Outline and blit the board
            board_outline_position = self.board_position - Vector2(20)
            board_outline_rect = board_outline_position.unwrap() + (self.total_board_size + Vector2(40)).unwrap()
            pygame.draw.rect(self.display, self.color_palette[2].unwrap(), board_outline_rect)
            self.display.blit(self.board_surface, self.board_position.unwrap())
            # Blit the pieces
            self.display.blit(self.pieces_surface, self.board_position.unwrap())

            self.clock.tick(self.fps)
            pygame.display.flip()

    def close_game(self):
        quit("Game closed")

    def mouse_click(self, position, button):
        """
        Global function that is called when the mouse is clicked somewhere on the screen\n
        Calls Piece.on_click(position, on_board_position, button) function of every piece, in order that they were created\n
        Calls Piece.clicked(button) function of a piece under the cursor when click happened instead of Piece.on_click()\n
        Enable Piece.allow_any_and_direct_click_in_one to call both functions on a piece at the same time if it was clicked (Piece.on_click() comes first)\n
        TODO: Make functions Piece.on_click() and Piece.clicked(), and make property Piece.allow_any_and_direct_click_in_one

        :param position: Vector2 position of the click on the screen
        :param button: Button that was pressed, 1 for left, 2 for middle and 3 for right
        """

        on_board_position = self.screen_to_board_position(position)
        click_on_board = 0 <= on_board_position.x < self.board.size.x and 0 <= on_board_position.y < self.board.size.y

        self.click_position = position

        for index, piece in enumerate(self.board.pieces):
            # if piece.position != on_board_position or piece.allow_any_and_direct_click_in_one:
            #   piece.on_click(position, on_board_position, button)

            if piece.position == on_board_position:
                #piece.clicked(button)

                pass

    def mouse_release(self, position, button):
        """
        Global function that is called when the mouse is released somewhere on the screen\n
        Calls Piece.on_click_release(position, on_board_position, button) function of every piece, in order that they were created\n
        Calls Piece.click_released(button) function of a piece under the cursor when release happened instead of Piece.on_click_release()\n
        BUT it calls Piece.click_released(button) only if the piece was the one clicked before\n
        Enable Piece.allow_any_and_direct_click_in_one to call both functions on a piece at the same time if it was clicked (Piece.on_click_release() comes first)\n
        TODO: Make functions Piece.on_click_release() and Piece.click_released()

        :param position: Vector2 position of the release point on the screen
        :param button: Button that was released, 1 for left, 2 for middle and 3 for right
        """

        on_board_position = self.screen_to_board_position(position)
        click_on_board = 0 <= on_board_position.x < self.board.size.x and 0 <= on_board_position.y < self.board.size.y

        on_same_place = on_board_position == self.board_click_position

        new_piece_selected = False

        # Deselect all pieces
        if button == 3:
            self.is_piece_selected = False

        self.is_piece_selected = False

        # Go through all pieces
        for index, piece in enumerate(self.board.pieces):
            #if piece.position != on_board_position or piece.allow_any_and_direct_click_in_one:
            #   piece.on_click_release(position, on_board_position, button)

            if piece.position == on_board_position:
                if on_same_place:
                    #piece.click_released(button)

                    # If piece is clicked, select it
                    if button == 1:
                        self.is_piece_selected = True
                        self.selected_piece = index
                        new_piece_selected = True

        if new_piece_selected:
            if self.is_piece_selected:
                # Set legal moves bitmap
                self.selected_legal_moves_bitmap = self.selected_piece_object.get_moves_raw(self.board.size)

                ally_pieces_bitmap = self.board.white_pieces_bitmap if self.selected_piece_object.is_white else self.board.black_pieces_bitmap

                self.selected_legal_moves_bitmap &= ~ally_pieces_bitmap
            else:
                self.selected_legal_moves_bitmap = 0

    def bitmap_to_positions(self, bitmap) -> list[Vector2]:
        """
        Use this to convert bitmaps (like from Piece.get_moves_raw()) to a list of positions on the board
        :param bitmap: A target bitmap, starts from top-left, and then goes like text - left-to-right and top-to-bottom
        :return: List of Vector2 positions that are on a bitmap
        """

        positions = []

        for i in range(self.board.size.area):
            bit = (bitmap >> i) % 2

            if bit:
                positions.append(Vector2(i % self.board.size.x, i // self.board.size.x))

        return positions

    def screen_to_board_position(self, position) -> Vector2:
        """
        Shorthand for (position - self.board_position) // self.board_cell_size\n
        :param position: Vector2 position on the screen
        :return: Vector2 position on the board
        """

        return (position - self.board_position) // self.board_cell_size

    def change_board_size(self, entire_board_size=None, single_cell_size=None, relative=True):
        """
        Method for changing the board size, single cell and entire board
        :param relative: Is change relative to previous values, True by default
        :param entire_board_size: Vector2 entire board size in cells
        :param single_cell_size: Vector2 single cell size in pixels
        """

        if entire_board_size is not None:
            self.board.size = Vector2(entire_board_size) if not relative else self.board.size + Vector2(entire_board_size)
        if single_cell_size is not None:
            self.board_cell_size = Vector2(single_cell_size) if not relative else self.board_cell_size + Vector2(single_cell_size)

        self.board_surface = pygame.Surface(self.total_board_size.unwrap()).convert_alpha()

        self.pieces_surface = pygame.Surface(self.total_board_size.unwrap()).convert_alpha()

        self.board_surface.fill(self.background_color.unwrap())
        self.pieces_surface.fill((0, 0, 0, 0))

    @property
    def selected_piece_object(self) -> Piece:
        """
        Shorthand for self.board.pieces[self.selected_piece]
        """

        return self.board.pieces[self.selected_piece]

    @property
    def click_position(self) -> Vector2:
        """
        Last click position on the screen
        """

        return self._click_position

    @click_position.setter
    def click_position(self, value):
        if not can_be_used_as_vector(value):
            raise ValueError("Click position is Vector2, so it can only be set to int, float, Vector2, Vector3, list, tuple and set")

        self._click_position = Vector2(value)

    @property
    def board_click_position(self) -> Vector2:
        """
        Last click position on the board
        """

        return self.screen_to_board_position(self.click_position)

    @property
    def window_resolution(self) -> Vector2:
        """
        Vector2 resolution of the main game window
        """
        return self._window_resolution

    @window_resolution.setter
    def window_resolution(self, value) -> None:
        if not can_be_used_as_vector(value):
            raise ValueError("Window resolution is Vector2, so it can only bet set to int, float, Vector2, Vector3, list, tuple and set")
        self._window_resolution = Vector2(value)

    @property
    def window_width(self) -> float:
        """
        Width of the main game window
        """
        return self.window_resolution.x

    @property
    def window_height(self) -> float:
        """
        Vector2 resolution of the main game window
        """
        return self.window_resolution.y

    @property
    def half_win_res(self) -> Vector2:
        """
        Vector2 half of the main game window resolution\n
        Shorthand for self.window_resolution / 2\n
        Read only
        """
        return self.window_resolution / 2

    @property
    def half_win_wid(self) -> float:
        """
        Half of the main game window height\n
        Shorthand for self.window_width / 2\n
        Read only
        """
        return self.window_width / 2

    @property
    def half_win_hei(self) -> float:
        """
        Half of the main game window width\n
        Shorthand for self.window_height / 2\n
        Read only
        """
        return self.window_height / 2

    @property
    def fps(self) -> float:
        """
        Frames per Second of the main game
        """
        return self._fps

    @fps.setter
    def fps(self, value) -> None:
        if not type(value) in [int, float]:
            raise ValueError("FPS is float, so it can only bet set to int and float")
        self._fps = value

    @property
    def display(self) -> pygame.surface.Surface:
        """
        Pygame Surface Main game display
        """
        return self._display

    @display.setter
    def display(self, value) -> None:
        if not isinstance(value, pygame.surface.Surface):
            raise ValueError("Display is a Pygame Surface, so it can only be set to pygame.surface.Surface")
        self._display = value

    @property
    def clock(self) -> pygame.time.Clock:
        """
        Pygame Clock Main game clock
        """
        return self._clock

    @clock.setter
    def clock(self, value) -> None:
        if not isinstance(value, pygame.time.Clock):
            raise ValueError("Clock is a pygame.time.Clock, so it can only be set to pygame.time.Clock")

        self._clock = value

    @property
    def background_color(self) -> Vector3:
        """
        Main game window background color
        """
        return self._background_color

    @background_color.setter
    def background_color(self, value) -> None:
        if not can_be_used_as_vector(value):
            raise ValueError("Background color is a Vector3, so it can only be set to int, float, Vector2, Vector3, list, tuple and set")
        self._background_color = Vector3(value)

    @property
    def total_board_size(self) -> Vector2:
        """
        Vector2 total size of the board (not including outline) in pixels\n
        Shorthand self.board.size * self.board_cell_size
        """
        return self.board.size * self.board_cell_size

    @property
    def color_palette(self) -> list[Vector3]:
        """
        The color palette of the game\n
        Has at least 4 colors (Vector3)\n
        You do not have to use it, but the base game does
        """
        return self._color_palette

    @color_palette.setter
    def color_palette(self, value) -> None:
        if not isinstance(value, list):
            raise ValueError("Color palette is a list of at least 4 colors (Vector3), so it can only be set to a list")
        if len(value) < 4:
            raise SyntaxError("Color palette is a list of at least 4 colors (Vector3), but new list contains only " + str(len(value)))

        all_values_are_colors = True
        for index, value_color in enumerate(value):
            all_values_are_colors = all_values_are_colors and isinstance(value_color, Vector3)
            if not all_values_are_colors:
                raise TypeError("Color palette is a list of at least 4 colors (Vector3), but element " + str(index) + " in new list is not a color (Vector3)")

        self._color_palette = value.copy()

    @property
    def board_cell_size(self) -> Vector2:
        """
        Vector2 size of one individual cell on a board
        """
        return self._board_cell_size

    @board_cell_size.setter
    def board_cell_size(self, value):
        if not can_be_used_as_vector(value):
            raise ValueError("Board cell size is a Vector2, so it can only be set to int, float, Vector2, Vector3, list, tuple and set")

        self._board_cell_size = value

    @property
    def white_cell_color(self) -> Vector3:
        """
        Vector3 main game white cells color
        """
        return self._white_cell_color

    @white_cell_color.setter
    def white_cell_color(self, value) -> None:
        if not can_be_used_as_vector(value):
            raise ValueError("White cell color is a Vector3, so it can only be set to int, float, Vector2, Vector3, list, tuple and set")
        self._white_cell_color = Vector3(value)

    @property
    def black_cell_color(self) -> Vector3:
        """
        Vector3 main game black cells color
        """
        return self._black_cell_color

    @black_cell_color.setter
    def black_cell_color(self, value) -> None:
        if not can_be_used_as_vector(value):
            raise ValueError("Black cell color is a Vector3, so it can only be set to int, float, Vector2, Vector3, list, tuple and set")
        self._black_cell_color = Vector3(value)

    @property
    def board_position(self) -> Vector2:
        """
        Vector2 position of top-left corner of the board in pixels on the main display
        """
        return self._board_position

    @board_position.setter
    def board_position(self, value) -> None:
        if not can_be_used_as_vector(value):
            raise ValueError("Board position is Vector2, so it can only bet set to int, float, Vector2, Vector3, list, tuple and set")
        self._board_position = Vector2(value)

    @property
    def board(self) -> Board:
        """
        The main game board object\n
        Does not include any visual components\n
        Only the board state and everything in it
        """
        return self._board

    @board.setter
    def board(self, value) -> None:
        if not isinstance(value, Board):
            raise ValueError("Board is a Board object, so it can only bet set to another Board object")

        self._board = value

    @property
    def board_surface(self) -> pygame.surface.Surface:
        """
        Board surface to draw the board on\n
        This is not a surface for pieces
        """
        return self._board_surface

    @board_surface.setter
    def board_surface(self, value):
        if not isinstance(value, pygame.surface.Surface):
            raise ValueError("Board surface is a Pygame Surface, so it can only be set to pygame.surface.Surface")

        self._board_surface = value

    @property
    def on_board_indicators_alpha(self) -> float:
        """
        Alpha channel of on-board indicators (like allowed moves, selected piece etc.)
        """
        return self._on_board_indicators_alpha

    @on_board_indicators_alpha.setter
    def on_board_indicators_alpha(self, value) -> None:
        if not type(value) in [int, float]:
            raise ValueError("On board indicators alpha is float, so it can only bet set to int and float")
        self._on_board_indicators_alpha = value


if __name__ == "__main__":
    game = Main(Vector2(1920, 1080), 120)
    game.run()
