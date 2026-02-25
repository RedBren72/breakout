# A simple pygame implementation of the ZX Spectrum game "Thru' The Wall"
# Pygame version by ChatGPT 4.0

import pygame
import random
import sys
import os
import time
from game import GameState

# Create the central GameState
state = GameState()

# Function to show intro screen
def showIntro():

    font = pygame.font.SysFont(None, 200)
    titleText = font.render("Breakout", True, state.rgbWHITE)
    font = pygame.font.SysFont(None, 50)
    directionText = font.render("Z for Left - X for Right SHIFT for Speed", True, state.rgbWHITE)
    instructionText = font.render("Press SPACE to Start", True, state.rgbWHITE)

    # create an array of colours to flash
    flashColours = [state.rgbGREEN, state.rgbCYAN, state.rgbBLUE, state.rgbMAGENTA, state.rgbRED, state.rgbYELLOW, state.rgbWHITE, state.rgbGREY224, state.rgbGREY192, state.rgbGREY160, state.rgbGREY128, state.rgbGREY096, state.rgbGREY064, state.rgbGREY032, state.rgbBLACK]

    # Flashing screen
    for colour in flashColours:
        state.gameScreen.fill( colour )
        if colour in flashColours[7:len(flashColours)]: # Only display text on the monochrome colours
            state.gameScreen.blit(titleText, (state.scrWIDTH // 2 - titleText.get_width() // 2, state.scrHEIGHT // 4))
        pygame.display.update()
        pygame.time.delay( 200 )

    state.gameScreen.fill( state.rgbBLACK )
    state.gameScreen.blit(titleText, (state.scrWIDTH // 2 - titleText.get_width() // 2, state.scrHEIGHT // 4))
    state.gameScreen.blit(directionText, (state.scrWIDTH // 2 - directionText.get_width() // 2, state.scrHEIGHT // 2))
    state.gameScreen.blit(instructionText, (state.scrWIDTH // 2 - instructionText.get_width() // 2, state.scrHEIGHT * 3 // 4))
    pygame.display.update()





# Main game loop
while not state.exit:
    state.gameClock = pygame.time.Clock()

    showIntro()

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
                    state.bat.set_direction(state.dirLEFT)
                if event.key == pygame.K_x:
                    state.bat.set_direction(state.dirRIGHT)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    state.bat.set_speed(state.scrSIZE // 4)
                if event.key == pygame.K_z or event.key == pygame.K_x:
                    state.bat.set_direction(state.dirSTOP)

            if event.type == pygame.QUIT:
                gameRunning = False
                state.exit = True 
                
        # Update bat position
        state.bat.update(state.scrWIDTH)

        # Update ball position
        state.ball.update(state.scrWIDTH, state.scrHEIGHT)

        # Check for missed ball
        state.ball.check_missed(state.scrWIDTH, state.scrHEIGHT)

        # Check for collision with wall
        score_from_wall = state.wall.check_collision(state.ball, state.scrWIDTH, state.level)
        state.score += score_from_wall

        # Check for collision with bat
        if state.bat.check_collision(state.ball):
            state.score += state.level
        
        # Draw everything
        state.gameScreen.fill( state.rgbCYAN )
        state.wall.draw(state.gameScreen)
        state.ball.draw(state.gameScreen)
        state.bat.draw(state.gameScreen)
        font = pygame.font.SysFont(None, 35)
        scoreText = font.render("Score: " + str(state.score), True, state.rgbBLACK)
        state.gameScreen.blit(scoreText, (10, state.scrHEIGHT - state.scrSIZE))
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
