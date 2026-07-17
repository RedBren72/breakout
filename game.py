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
    width: int = scrWIDTH
    height: int = scrHEIGHT

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
            random.randint(-scrSIZE * 5, scrSIZE * 5) + self.width // 2,
            self.height // 2,
            scrSIZE // 2,
            dirSTOP,
            dirDOWN,
            rgbBLACK,
        )

        self.bat = Bat(
            (self.width // 2) - scrSIZE // 2,
            self.height - scrSIZE * 3,
            scrSIZE * 4,
            scrSIZE,
            rgbBLACK,
        )

        self.wall = Wall(self.width, self.height, scrSIZE)

        pygame.init()
        self.gameDisplay = pygame.display
        self.gameDisplay.set_caption("Breakout")
        self.gameScreen = self.gameDisplay.set_mode((self.width, self.height))
        self.gameClock = pygame.time.Clock()

    def reset_wall(self):
        self.wall.reset()
