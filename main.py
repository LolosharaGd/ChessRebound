import pygame
from Morztypes import Vector2, Vector3
from board import *

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

        self.color_palette = [Vector3(243, 238, 234), Vector3(235, 227, 213), Vector3(176, 166, 149), Vector3(119, 107, 93)]

        self._background_color = self.color_palette[0]

        self.board_cell_size = Vector2(100, 100)
        self.white_cell_color = self.color_palette[1]
        self.black_cell_color = self.color_palette[2]
        self.board_position = Vector2(140, 140)

        self.board = Board(Vector2(8, 8))

        self.board_surface = pygame.Surface(self.total_board_size.unwrap())

    def run(self):
        """
        Main game loop function
        """

        while True:
            self.display.fill(self.background_color.unwrap())

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.close_game()

                elif e.type == pygame.KEYDOWN:
                    if e.unicode == "":
                        self.close_game()

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

            # Blit the surfaces

            # Outline and blit the board
            board_outline_position = self.board_position - Vector2(20)
            board_outline_rect = board_outline_position.unwrap() + (self.total_board_size + Vector2(40)).unwrap()
            pygame.draw.rect(self.display, self.color_palette[2].unwrap(), board_outline_rect)
            self.display.blit(self.board_surface, self.board_position.unwrap())

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
        if  not Vector3.can_be_used(value):
            raise ValueError("Window resolution is Vector2, so it can only bet set to int, float, Vector2, Vector3, list, tuple and set")
        self._window_resolution = Vector3(value)

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
            raise ValueError("Display is a Pygame Surface, so itt can only be set to pygame.surface.Surface")
        self._display = value

    @property
    def clock(self) -> pygame.time.Clock:
        """
        Pygame Clock Main game clock
        """
        return self._clock

    @clock.setter
    def clock(self, value) -> None:
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
        return self.board_size * self.board_cell_size


if __name__ == "__main__":
    game = Main(Vector2(1920, 1080), 120)
    game.run()
