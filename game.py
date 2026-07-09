from dataclasses import dataclass, field
import random
import pygame

from ball import Ball
from bat import Bat
from wall import Wall
from constants import (scrWIDTH, scrHEIGHT, scrSIZE, scrAREA, rgbBLACK,
                       dirSTOP, dirDOWN)


@dataclass
class GameState:
    gameSpeed: int = field(default_factory=lambda: scrHEIGHT // 5)
    score: int = 0
    level: int = 1
    exit: bool = False
    keyPressed: bool = False

    # runtime objects
    ball: Ball = None
    bat: Bat = None
    wall: Wall = None
    gameDisplay = None
    gameScreen = None
    gameClock = None

    def __post_init__(self):
        # create game objects
        self.ball = Ball(
            random.randint(-scrSIZE * 5, scrSIZE * 5) + scrWIDTH // 2,
            scrHEIGHT // 2,
            scrSIZE // 2,
            dirSTOP,
            dirDOWN,
            rgbBLACK,
        )

        self.bat = Bat(
            (scrWIDTH // 2) - scrSIZE // 2,
            scrHEIGHT - scrSIZE * 3,
            scrSIZE * 4,
            scrSIZE,
            rgbBLACK,
        )

        self.wall = Wall(scrWIDTH, scrHEIGHT, scrSIZE)

        pygame.init()
        self.gameDisplay = pygame.display
        self.gameDisplay.set_caption("Breakout")
        self.gameScreen = self.gameDisplay.set_mode(scrAREA)
        self.gameClock = pygame.time.Clock()

    def reset_wall(self):
        self.wall.reset()
