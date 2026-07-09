import pygame
from ball import Ball
from bat import Bat
from constants import dirLEFT, dirRIGHT, dirSTOP

pygame.init()

def run_case(name, bat, ball):
    print(f"--- {name} ---")
    print(f"Before: ball.x={ball.x}, dx={ball.dx}, dy={ball.dy}")
    collided = bat.check_collision(ball)
    print(f"Collided: {collided}")
    print(f"After:  ball.x={ball.x}, dx={ball.dx}, dy={ball.dy}\n")

# Setup bat
bat = Bat(50, 100, 80, 10, (0,0,0))

# Case A: corner bounce (left corner) - moving left into left corner
ball = Ball(bat.x + 2, bat.y - 5 + 1, 5, -2, 3, (0,0,0))
run_case("Corner bounce left (diag into corner)", bat, ball)

# Case B: hitting leftmost part from left -> straight up
ball = Ball(bat.x + 2, bat.y - 5 + 1, 5, 2, 3, (0,0,0))
run_case("Hit leftmost from left (straight up)", bat, ball)

# Case C: falling straight down hitting left half -> go left
ball = Ball(bat.x + 10, bat.y - 5 + 1, 5, 0, 3, (0,0,0))
run_case("Falling straight down on left half (should go left)", bat, ball)

# Case D: falling straight down hitting right half -> go right
ball = Ball(bat.x + 70, bat.y - 5 + 1, 5, 0, 3, (0,0,0))
run_case("Falling straight down on right half (should go right)", bat, ball)

# Case E: corner bounce right (diag into right corner)
ball = Ball(bat.x + bat.width - 2, bat.y - 5 + 1, 5, 2, 3, (0,0,0))
run_case("Corner bounce right (diag into corner)", bat, ball)

pygame.quit()
