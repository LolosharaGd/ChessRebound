import pygame
from Morztypes import Vector2, Vector3
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

        self._board_cell_size = Vector2(100, 100)
        self._white_cell_color = self.color_palette[1]
        self._black_cell_color = self.color_palette[2]
        self._board_position = Vector2(140, 140)

        self._board = Board(Vector2(8, 8))

        self._board_surface = pygame.Surface(self.total_board_size.unwrap()).convert_alpha()

        self.pieces_surface = pygame.Surface(self.total_board_size.unwrap()).convert_alpha()

        self.textures = {
            Piece.White + Piece.Knight: pygame.image.load("Textures\\KnightWhite.png"),
            Piece.Black + Piece.Knight: pygame.image.load("Textures\\KnightBlack.png")
        }

    def run(self):
        """
        Main game loop function
        """

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

                    elif e.unicode == "a":
                        self.board.pieces.append(Knight(Vector2(2, 3), True))

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

            # Draw the pieces
            for piece in self.board.pieces:
                piece_position = piece.position * self.board_cell_size
                self.pieces_surface.blit(pygame.transform.scale(self.textures[piece.value], self.board_cell_size.unwrap()), piece_position.unwrap())

                # Debug - draw every piece's raw moves
                print(piece.get_moves_raw(self.board.size))

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

    @property
    def window_resolution(self) -> Vector2:
        """
        Vector2 resolution of the main game window
        """
        return self._window_resolution

    @window_resolution.setter
    def window_resolution(self, value) -> None:
        if not Vector3.can_be_used(value):
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
        if not Vector3.can_be_used(value):
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
        if not Vector2.can_be_used(value):
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
        if not Vector3.can_be_used(value):
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
        if not Vector3.can_be_used(value):
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
        if not Vector3.can_be_used(value):
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


if __name__ == "__main__":
    game = Main(Vector2(1920, 1080), 120)
    game.run()
