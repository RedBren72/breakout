import pygame
from constants import rgbRED, rgbGREEN, rgbBLUE, rgbYELLOW, rgbMAGENTA, rgbBLACK

class Wall:
    def __init__(self, screen_width, screen_height, brick_size, start_row=3):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.brick_size = brick_size
        self.start_row = start_row
        self.bricks = []
        self.brick_colours = [rgbRED, rgbGREEN, rgbMAGENTA, rgbYELLOW, rgbBLUE]
        self.create_bricks()
    
    def create_bricks(self):
        """Create the wall with bricks"""
        self.bricks = []
        for row in range(5):
            brick_row = []
            yPos = (self.start_row + row) * self.brick_size
            
            if row % 2 == 0:
                # Even row - full bricks only
                for col in range(self.screen_width // (self.brick_size * 2)):
                    xPos = col * self.brick_size * 2
                    brick_rect = pygame.Rect(xPos, yPos, self.brick_size * 2, self.brick_size)
                    brick_row.append((brick_rect, self.brick_colours[row]))
            else:
                # Odd row - half-bricks at start and end
                half_brick_rect_start = pygame.Rect(0, yPos, self.brick_size, self.brick_size)
                brick_row.append((half_brick_rect_start, self.brick_colours[row]))
                
                for col in range(1, (self.screen_width // (self.brick_size * 2))):
                    xPos = col * self.brick_size * 2 - self.brick_size
                    brick_rect = pygame.Rect(xPos, yPos, self.brick_size * 2, self.brick_size)
                    brick_row.append((brick_rect, self.brick_colours[row]))
                
                half_brick_rect_end = pygame.Rect(self.screen_width - self.brick_size, yPos, self.brick_size, self.brick_size)
                brick_row.append((half_brick_rect_end, self.brick_colours[row]))
            
            self.bricks.append(brick_row)
    
    def draw(self, screen):
        """Draw all bricks on screen"""
        for row in self.bricks:
            for brick, colour in row:
                pygame.draw.rect(screen, colour, brick)
                pygame.draw.rect(screen, rgbBLACK, brick, 4)  # Black border
    
    def check_collision(self, ball_obj, screen_size, game_level):
        """Check if ball has hit a brick and handle collision"""
        score_increase = 0
        
        for row_idx, row in enumerate(self.bricks):
            for brick_idx, (brick, colour) in enumerate(row):
                # Create a rect for the ball's current position
                ball_rect = pygame.Rect(
                    ball_obj.x - ball_obj.radius,
                    ball_obj.y - ball_obj.radius,
                    ball_obj.radius * 2,
                    ball_obj.radius * 2
                )
                
                if brick.colliderect(ball_rect):
                    # Update score based on game level and row of brick hit
                    score_increase = 5 * (len(self.bricks) - row_idx + game_level)
                    
                    # Determine which side of the brick was hit
                    # Find the overlap areas to determine the collision side
                    overlap_left = (ball_rect.right - brick.left) if ball_rect.right > brick.left else float('inf')
                    overlap_right = (brick.right - ball_rect.left) if ball_rect.left < brick.right else float('inf')
                    overlap_top = (ball_rect.bottom - brick.top) if ball_rect.bottom > brick.top else float('inf')
                    overlap_bottom = (brick.bottom - ball_rect.top) if ball_rect.top < brick.bottom else float('inf')
                    
                    # Find the minimum overlap to determine the collision side
                    min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)
                    
                    if min_overlap == overlap_top or min_overlap == overlap_bottom:
                        # Hit top or bottom of brick
                        ball_obj.dy = -ball_obj.dy
                    else:
                        # Hit left or right of brick
                        ball_obj.dx = -ball_obj.dx
                    
                    # Remove the brick
                    row.pop(brick_idx)
                    return score_increase
        
        return score_increase
    
    def reset(self):
        """Reset the wall for a new game"""
        self.create_bricks()
