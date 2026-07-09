import pygame
import random
from constants import scrWIDTH, scrHEIGHT, scrSIZE, dirSTOP, dirDOWN

class Ball:
    def __init__(self, x, y, radius, dx, dy, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.dx = dx # Velocity in x
        self.dy = dy # Velocity in y
        self.color = color
    def update(self):
        # Move the ball
        self.x += self.dx
        self.y += self.dy

        # Bounce off left/right edges
        if self.x - self.radius < 0:
            self.dx = -self.dx
            self.x = self.radius
        elif self.x + self.radius > scrWIDTH:
            self.dx = -self.dx
            self.x = scrWIDTH - self.radius
        
        # Bounce off top edge (bottom edge is handled by missed ball detection)
        if self.y - self.radius < 0:
            self.dy = -self.dy
            self.y = self.radius
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
    
    def reset(self):
        """Reset ball to from a random starting position"""
        self.x = random.randint(-scrSIZE * 5, scrSIZE * 5) + scrWIDTH // 2
        self.y = scrHEIGHT // 2
        self.dx = dirSTOP
        self.dy = dirDOWN
    
    def check_missed(self):
        """Check if ball has been missed and reset if necessary"""
        if self.y > scrHEIGHT - scrSIZE * 2.5:
            self.reset()
