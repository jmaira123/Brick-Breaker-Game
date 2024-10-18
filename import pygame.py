import pygame
import random
import time

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
BALL_RADIUS = 10
BRICK_WIDTH, BRICK_HEIGHT = 75, 20
ROWS, COLS = 5, 10
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Set up screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout (Brick Breaker)")
clock = pygame.time.Clock()

# Font for displaying score and timer
font = pygame.font.Font(None, 36)

# Paddle Class
class Paddle:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 30, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = 8

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def draw(self):
        pygame.draw.rect(screen, BLUE, self.rect)

# BALL CLASS
class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
        self.dx = random.choice([-4, 4])
        self.dy = -4
        self.touches = 0 

    def move(self, paddle):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Wall collision
        if self.rect.left <= 0  or self.rect.right >= WIDTH:
           self.dx = -self.dx
        if self.rect.top <=0:
            self.dy = -self.dy
        if self.rect.bottom >= HEIGHT:
            return True 

            # Paddle  collision
        if self.rect.colliderect(paddle.rect):
            self.dy = -self.dy
            self.touches += 1

        return False

    def draw(self):
        pygame.draw.ellipse(screen, WHITE, self.rect)

# Brick class
class Brick:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)

    def draw(self):
        pygame.draw.rect(screen, RED, self.rect)

# Game loop
def main():
    paddle = Paddle()
    ball = Ball()

    # Create bricks
    bricks = [Brick(x * (BRICK_WIDTH + 5) + 20, y * (BRICK_HEIGHT + 5) + 50) for x in range(COLS) for y in range(ROWS)]

    running = True
    lives = 3
    score = 0
    misses = 0
    game_start_time = time.time()

    while running:
        clock.tick(FPS)
        screen.fill(BLACK)

        # Update game time
        elapsed_time = time.time() - game_start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)

        # Prepare texts for displaying
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        misses_text = font.render(f"Misses: {misses}", True, WHITE)
        touches_text = font.render(f"Touches: {ball.touches}", True, WHITE)
        timer_text = font.render(f"Time: {minutes}: {seconds:02d}", True, WHITE)
        score_text = font.render(f"Score: {score}", True, WHITE)

        #Organize UI element in a single lines with added space
        screen.blit(lives_text, (10, 10))
        screen.blit(misses_text, (160, 10))
        screen.blit(touches_text, (320, 10))
        screen.blit(timer_text, (450, 10))
        screen.blit(score_text, (600, 10))

        # Add space for bricks
        brick_y_offset = 50

        remaining_bricks = len(bricks)

        #End game if no bricks remain
        if remaining_bricks == 0:
            win_time_text = font.render(f"You Win! Time: {minutes}:{seconds:02d}", True, WHITE)
            screen.blit(win_time_text, (WIDTH // 2 - 150, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False 

        # Ball movement and drawing
        if ball.move(paddle):
            lives -= 1
            misses += 1
            if lives == 0:
                running = False
            ball.rect.topleft = (WIDTH // 2, HEIGHT // 2)

        ball.draw()
        paddle.move()
        paddle.draw()

        # Brick colliion
        for brick in bricks[:]:
            if ball.rect.colliderect(brick.rect):
                bricks.remove(brick)
                ball.dy = -ball.dy
                score += 1
                break

        #Draw bricks with adjusted position
        for brick in bricks:
            brick.draw()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()



