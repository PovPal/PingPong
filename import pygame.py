import pygame
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BALL_RADIUS = 15
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")

# Clock
clock = pygame.time.Clock()

# Paddle Class
class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.speed = 5
    
    def move(self, up=False, down=False):
        if up and self.y > 0:
            self.y -= self.speed
        if down and self.y < HEIGHT - self.height:
            self.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))

# Ball Class
class Ball:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.radius = BALL_RADIUS
        self.x_speed = random.choice([5, -5])
        self.y_speed = random.choice([5, -5])
    
    def move(self):
        self.x += self.x_speed
        self.y += self.y_speed
        
        # Collision with top and bottom
        if self.y <= 0 or self.y >= HEIGHT - self.radius:
            self.y_speed = -self.y_speed
        
    def draw(self):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.radius)

# Display "Player X Lost" message
def display_loss_message(player):
    font = pygame.font.SysFont('arial', 50)
    text = font.render(f"Player {player} Won", True, GREEN)
    screen.blit(text, (WIDTH // 4, HEIGHT // 2 - 50))
    pygame.display.flip()
    pygame.time.delay(2000)  # Show for 2 seconds

# Main Game Function
def game():
    # Create paddles and ball
    paddle_left = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    paddle_right = Paddle(WIDTH - 30, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    ball = Ball()

    running = True
    while running:
        screen.fill(BLACK)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle paddle movements
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            paddle_left.move(up=True)
        if keys[pygame.K_s]:
            paddle_left.move(down=True)
        if keys[pygame.K_UP]:
            paddle_right.move(up=True)
        if keys[pygame.K_DOWN]:
            paddle_right.move(down=True)

        # Move the ball
        ball.move()

        # Ball and paddle collision
        if (ball.x - ball.radius <= paddle_left.x + paddle_left.width and
            paddle_left.y <= ball.y <= paddle_left.y + paddle_left.height):
            ball.x_speed = -ball.x_speed
            ball.x = paddle_left.x + paddle_left.width + ball.radius  # Prevent sticking

        if (ball.x + ball.radius >= paddle_right.x and
            paddle_right.y <= ball.y <= paddle_right.y + paddle_right.height):
            ball.x_speed = -ball.x_speed
            ball.x = paddle_right.x - ball.radius  # Prevent sticking

        # Check for loss condition (ball crosses left or right side)
        if ball.x <= 0:  # Left side - Player Right wins
            display_loss_message("Right")
            ball = Ball()  # Reset ball position
            paddle_left.y = HEIGHT // 2 - PADDLE_HEIGHT // 2
            paddle_right.y = HEIGHT // 2 - PADDLE_HEIGHT // 2
        elif ball.x >= WIDTH:  # Right side - Player Left wins
            display_loss_message("Left")
            ball = Ball()  # Reset ball position
            paddle_left.y = HEIGHT // 2 - PADDLE_HEIGHT // 2
            paddle_right.y = HEIGHT // 2 - PADDLE_HEIGHT // 2

        # Draw paddles, ball
        paddle_left.draw()
        paddle_right.draw()
        ball.draw()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# Run the game
game()
