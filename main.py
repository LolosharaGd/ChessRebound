import pygame as pg
from Morztypes import Vector2, Vector3

pg.init()


class Main:
    """
    Main game class, contains main game loop function "run()" and other global variables
    """

    def __init__(self, resolution=Vector2(1920, 1080), fps=120):
        self._window_resolution = resolution

        self._fps = fps

        self._display = pg.display.set_mode(resolution.unwrap())

        self._clock = pg.time.Clock()

    def run(self):
        """
        Main game loop function
        """

        while True:
            self.display.fill(Vector3(0, 0, 0).unwrap())

            for e in pg.event.get():
                if e.type == pg.QUIT:
                    self.close_game()

                elif e.type == pg.KEYDOWN:
                    if e.unicode == "":
                        self.close_game()

            self.clock.tick(self.fps)
            pg.display.flip()

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
        if not type(value) in [int, float, Vector2, Vector3, list, tuple, set]:
            raise ValueError("Window resolution is Vector2, so it can only bet set to int, float, Vector2, Vector3, list, tuple and set")
        self._window_resolution = value

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
    def display(self) -> pg.surface.Surface:
        """
        Pygame Surface Main game display
        """
        return self._display

    @display.setter
    def display(self, value) -> None:
        self._display = value

    @property
    def clock(self) -> pg.time.Clock:
        """
        Pygame Clock Main game clock
        """
        return self._clock

    @clock.setter
    def clock(self, value) -> None:
        self._clock = value


if __name__ == "__main__":
    game = Main(Vector2(1920, 1080), 120)
    game.run()
