# A simple pygame implementation of the ZX Spectrum game "Thru' The Wall"
# Pygame version by ChatGPT 4.0

import pygame
import random
import sys
import os
import time
from game import GameState
from constants import (rgbWHITE, rgbGREEN, rgbCYAN, rgbBLUE, rgbMAGENTA, rgbRED,
                       rgbYELLOW, rgbGREY224, rgbGREY192, rgbGREY160, rgbGREY128,
                       rgbGREY096, rgbGREY064, rgbGREY032, rgbBLACK, dirLEFT, dirRIGHT, dirSTOP)

# Create the central GameState
state = GameState()

# Function to show intro screen
def show_intro(game_state):
    font_large = pygame.font.SysFont(None, 200)
    font_medium = pygame.font.SysFont(None, 50)
    title_text = font_large.render("Breakout", True, rgbWHITE)
    direction_text = font_medium.render("Z for Left - X for Right SHIFT for Speed", True, rgbWHITE)
    instruction_text = font_medium.render("Press SPACE to Start", True, rgbWHITE)

    flash_colours = [rgbGREEN, rgbCYAN, rgbBLUE, rgbMAGENTA, rgbRED, rgbYELLOW,
                     rgbWHITE, rgbGREY224, rgbGREY192, rgbGREY160, rgbGREY128,
                     rgbGREY096, rgbGREY064, rgbGREY032, rgbBLACK]
    
    last_flash_time = pygame.time.get_ticks()
    flash_delay = 200  # ms
    color_index = 0

    # Flashing screen until a key is pressed
    while color_index < len(flash_colours):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                return False # Signal to exit
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return True # Signal to start

        current_time = pygame.time.get_ticks()
        if current_time - last_flash_time > flash_delay:
            colour = flash_colours[color_index]
            game_state.gameScreen.fill(colour)
            if colour in flash_colours[7:]:  # Only display text on the monochrome colours
                game_state.gameScreen.blit(title_text, (game_state.scrWIDTH // 2 - title_text.get_width() // 2, game_state.scrHEIGHT // 4))
            pygame.display.update()
            last_flash_time = current_time
            color_index += 1

    # Final static screen
    game_state.gameScreen.fill(rgbBLACK)
    game_state.gameScreen.blit(title_text, (game_state.scrWIDTH // 2 - title_text.get_width() // 2, game_state.scrHEIGHT // 4))
    game_state.gameScreen.blit(direction_text, (game_state.scrWIDTH // 2 - direction_text.get_width() // 2, game_state.scrHEIGHT // 2))
    game_state.gameScreen.blit(instruction_text, (game_state.scrWIDTH // 2 - instruction_text.get_width() // 2, game_state.scrHEIGHT * 3 // 4))
    pygame.display.update()
    return True

# Main game loop
while not state.exit:
    state.gameClock = pygame.time.Clock()

    if not show_intro(state):
        state.exit = True
        break

    # Menu loop
    menu = True
    # If AUTO_START is set, bypass menu and start immediately
    if os.getenv('AUTO_START'):
        gameRunning = True
        menu = False
    else:
        while menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_SPACE:
                        gameRunning = True
                        menu = False
                    
    state.reset_wall()

    # Game loop
    while gameRunning:
        # If AUTO_RUN_SECONDS is set, set up a start time and timeout once
        if os.getenv('AUTO_RUN_SECONDS') and not hasattr(state, '_auto_start_time'):
            try:
                state._auto_run_timeout = float(os.getenv('AUTO_RUN_SECONDS'))
            except ValueError:
                state._auto_run_timeout = None
            state._auto_start_time = time.time()

        # Get keypresses
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    gameRunning = False
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    state.bat.set_speed(state.scrSIZE // 2)                   
                if event.key == pygame.K_z:
                    state.bat.set_direction(dirLEFT)
                if event.key == pygame.K_x:
                    state.bat.set_direction(dirRIGHT)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    state.bat.set_speed(state.scrSIZE // 4)
                if event.key == pygame.K_z or event.key == pygame.K_x:
                    state.bat.set_direction(dirSTOP)

            if event.type == pygame.QUIT:
                gameRunning = False
                state.exit = True 
                
        # Update bat position
        state.bat.update()

        # Update ball position
        state.ball.update()

        # Check for missed ball
        state.ball.check_missed()

        # Check for collision with wall
        score_from_wall = state.wall.check_collision(state.ball, state.scrWIDTH, state.level)
        state.score += score_from_wall

        # Check for collision with bat
        if state.bat.check_collision(state.ball):
            state.score += state.level
        
        # Draw everything
        state.gameScreen.fill(rgbCYAN)
        state.wall.draw(state.gameScreen)
        state.ball.draw(state.gameScreen)
        state.bat.draw(state.gameScreen)
        font = pygame.font.SysFont(None, 35)
        scoreText = font.render("Score: " + str(state.score), True, rgbBLACK)
        state.gameScreen.blit(scoreText, (10, state.wall.screen_height - state.wall.brick_size))
        pygame.display.update()        
        
        state.gameClock.tick( state.gameSpeed )
        # Auto-run check: if AUTO_RUN_SECONDS was set, stop after elapsed time
        if hasattr(state, '_auto_start_time') and getattr(state, '_auto_run_timeout', None) is not None:
            if (time.time() - state._auto_start_time) >= state._auto_run_timeout:
                gameRunning = False
                state.exit = True
                break
        
    state.exit = True

    

print( "Exiting..." )
pygame.quit()
sys.exit()
