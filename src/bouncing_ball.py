import pygame
import sys
import math
import random

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Objects Animation")

# Colors
GREEN = (50, 205, 50)
WHITE = (255, 255, 255)

# Circle boundary
CIRCLE_RADIUS = 300
CIRCLE_CENTER = (WIDTH // 2, HEIGHT // 2)

# Exit zone
EXIT_WIDTH = 100
EXIT_HEIGHT = 100
EXIT_POS = (CIRCLE_CENTER[0] - CIRCLE_RADIUS, CIRCLE_CENTER[1])

# Load and scale logo images
logo1 = pygame.image.load("logo.svg")  # Replace with your image paths
logo2 = pygame.image.load("logo.svg")
LOGO_SIZE = (60, 60)
logo1 = pygame.transform.scale(logo1, LOGO_SIZE)
logo2 = pygame.transform.scale(logo2, LOGO_SIZE)


# Object properties
class BouncingObject:
    def __init__(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 10
        self.angle = random.uniform(0, 2 * math.pi)
        self.escaped = False


    def update(self):
        if self.escaped:
            return

        # Move according to angle
        dx = math.cos(self.angle) * self.speed
        dy = math.sin(self.angle) * self.speed
        self.rect.x += dx
        self.rect.y += dy

        # Calculate distance from center
        distance = math.sqrt((self.rect.centerx - CIRCLE_CENTER[0]) ** 2 +
                             (self.rect.centery - CIRCLE_CENTER[1]) ** 2)

        # Check if near exit
        if math.dist((self.rect.centerx, self.rect.centery), EXIT_POS) < 50:
            self.escaped = True
            return

        # Check if hitting circle boundary
        if distance + self.rect.width // 2 > CIRCLE_RADIUS:
            # Calculate normal vector from center to object
            nx = (self.rect.centerx - CIRCLE_CENTER[0]) / distance
            ny = (self.rect.centery - CIRCLE_CENTER[1]) / distance

            # Reflect velocity vector along normal vector
            dot_product = nx * math.cos(self.angle) + ny * math.sin(self.angle)
            self.angle = self.angle - 2 * dot_product * math.acos(dot_product)

            # Pull back inside boundary
            self.rect.centerx = CIRCLE_CENTER[0] + nx * (CIRCLE_RADIUS - self.rect.width // 2)
            self.rect.centery = CIRCLE_CENTER[1] + ny * (CIRCLE_RADIUS - self.rect.height // 2)


# Create objects
obj1 = BouncingObject(logo1, WIDTH // 2 - 50, HEIGHT // 2)
obj2 = BouncingObject(logo2, WIDTH // 2 + 50, HEIGHT // 2)

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill background
    screen.fill(GREEN)

    # Draw circle boundary
    pygame.draw.circle(screen, WHITE, CIRCLE_CENTER, CIRCLE_RADIUS, 3)

    # Draw exit
    pygame.draw.rect(screen, (200, 200, 200, 128),
                     (EXIT_POS[0] - EXIT_WIDTH // 2, EXIT_POS[1] - EXIT_HEIGHT // 2,
                      EXIT_WIDTH, EXIT_HEIGHT), 2)

    # Update and draw objects
    obj1.update()
    obj2.update()
    screen.blit(obj1.image, obj1.rect)
    screen.blit(obj2.image, obj2.rect)

    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()