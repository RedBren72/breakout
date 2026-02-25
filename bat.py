import pygame

class Bat:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.direction = 0
        self.speed = 4
    
    def update(self, width):
        """Update bat position based on direction and speed"""
        self.x += self.speed * self.direction
        
        # Keep bat within screen bounds
        if self.x < 0:
            self.x = 0
        if self.x > width - self.width:
            self.x = width - self.width
    
    def set_direction(self, direction):
        """Set the direction of movement"""
        self.direction = direction
    
    def set_speed(self, speed):
        """Set the speed of movement"""
        self.speed = speed
    
    def get_rect(self):
        """Return pygame Rect for collision detection"""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, screen):
        """Draw the bat on screen"""
        pygame.draw.rect(screen, self.color, self.get_rect())
    
    def check_collision(self, ball_obj):
        """Check for collision with ball and handle bouncing"""
        # Import direction constants here to avoid circular imports at module load
        from game import dirSTOP, dirLEFT, dirRIGHT
        import os
        debug = bool(os.getenv("DEBUG_COLLISION"))
        ball_rect = pygame.Rect(ball_obj.x - ball_obj.radius, ball_obj.y - ball_obj.radius, ball_obj.radius * 2, ball_obj.radius * 2)
        if not self.get_rect().colliderect(ball_rect):
            return False

        # Only handle collisions when the ball is moving downwards (falling onto the bat)
        if ball_obj.dy <= 0:
            return False

        # Determine where on the bat the ball hit (use contact point for more accurate corner detection)
        rel_x = ball_obj.x - self.x  # center-based
        # leading/contact x depending on horizontal movement
        if ball_obj.dx < 0:
            contact_x = ball_obj.x - ball_obj.radius
        elif ball_obj.dx > 0:
            contact_x = ball_obj.x + ball_obj.radius
        else:
            contact_x = ball_obj.x
        rel_x_contact = contact_x - self.x
        # define corner zone as either a fraction of bat width or based on ball size
        corner_zone = max(self.width * 0.15, ball_obj.radius * 2)

        left_corner = rel_x_contact <= corner_zone
        right_corner = rel_x_contact >= (self.width - corner_zone)
        left_half = rel_x_contact < (self.width / 2)

        # 1) Aggressive corner bounce: if the contact point is inside the corner zone,
        # reflect both axes regardless of incoming horizontal direction. This makes
        # corner hits feel more responsive/elastic.
        if left_corner or right_corner:
            if debug:
                print(f"collision: corner_reflect_aggressive rel_x={rel_x:.1f} rel_x_contact={rel_x_contact:.1f} corner_zone={corner_zone:.1f} dx_in={ball_obj.dx} dy_in={ball_obj.dy}")
            # Reverse both velocity components
            ball_obj.dx = -ball_obj.dx
            ball_obj.dy = -ball_obj.dy
            if debug:
                print(f"collision: corner_reflect_aggressive dx_out={ball_obj.dx} dy_out={ball_obj.dy}")
            return True

        # 2) Hitting the extreme edge from the outside should send the ball straight up
        # If ball is approaching the bat from outside horizontally into the extreme edge
        if (left_corner and ball_obj.dx > 0 and ball_obj.x < self.x + self.width/2) or (right_corner and ball_obj.dx < 0 and ball_obj.x > self.x + self.width/2):
            if debug:
                print(f"collision: edge_up rel_x={rel_x:.1f} corner_zone={corner_zone:.1f} dx_in={ball_obj.dx} dy_in={ball_obj.dy}")
            ball_obj.dx = dirSTOP
            ball_obj.dy = -ball_obj.dy
            if debug:
                print(f"collision: edge_up dx_out={ball_obj.dx} dy_out={ball_obj.dy}")
            return True

        # 3) If the ball is falling straight down and hits left/right half, give it horizontal velocity
        if ball_obj.dx == dirSTOP:
            if debug:
                print(f"collision: straight_down rel_x={rel_x:.1f} left_half={left_half} dx_in={ball_obj.dx} dy_in={ball_obj.dy}")
            if left_half:
                ball_obj.dx = dirLEFT
            else:
                ball_obj.dx = dirRIGHT
            ball_obj.dy = -ball_obj.dy
            if debug:
                print(f"collision: straight_down dx_out={ball_obj.dx} dy_out={ball_obj.dy}")
            return True

        # 4) Default: invert vertical direction
        if debug:
            print(f"collision: default_up rel_x={rel_x:.1f} dx_in={ball_obj.dx} dy_in={ball_obj.dy}")
        ball_obj.dy = -ball_obj.dy
        if debug:
            print(f"collision: default_up dx_out={ball_obj.dx} dy_out={ball_obj.dy}")
        return True
