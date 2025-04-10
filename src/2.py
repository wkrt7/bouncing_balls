import pygame
import sys
import random
import math
from abc import ABC, abstractmethod
from typing import Protocol, Tuple, List, Optional
import os

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600  # Vertical video format for TikTok/Instagram
FPS = 60
GRAVITY = 0.5
BOUNCE_DAMPENING = 0.85  # Energy loss on bounce
MAX_INITIAL_VELOCITY = 15
BG_COLOR = (10, 10, 40)  # Dark blue background


# Define Boundary Protocol
class Boundary(Protocol):
    @abstractmethod
    def is_inside(self, position: Tuple[float, float]) -> bool:
        pass

    @abstractmethod
    def get_normal(self, position: Tuple[float, float]) -> Tuple[float, float]:
        pass

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        pass


# Circle Boundary Implementation
class CircleBoundary:
    def __init__(self, center: Tuple[int, int], radius: int, color: Tuple[int, int, int] = (255, 255, 255)):
        self.center = center
        self.radius = radius
        self.color = color
        self.thickness = 6  # Border thickness
        self.glow_colors = [
            (230, 0, 115),  # Pink
            (252, 185, 0),  # Gold
            (64, 224, 208)  # Turquoise
        ]
        self.glow_thickness = 15
        self.glow_radius_offset = 5
        self.glow_index = 0
        self.glow_speed = 0.02
        self.glow_timer = 0

    def is_inside(self, position: Tuple[float, float]) -> bool:
        dx = position[0] - self.center[0]
        dy = position[1] - self.center[1]
        distance_squared = dx * dx + dy * dy
        return distance_squared < (self.radius - 30) ** 2  # 30px buffer for object size

    def get_normal(self, position: Tuple[float, float]) -> Tuple[float, float]:
        dx = position[0] - self.center[0]
        dy = position[1] - self.center[1]
        distance = math.sqrt(dx * dx + dy * dy)
        if distance == 0:
            return (0, -1)  # Default normal if at center
        return (dx / distance, dy / distance)

    def draw(self, surface: pygame.Surface) -> None:
        # Update glow effect
        self.glow_timer += self.glow_speed
        glow_blend = abs(math.sin(self.glow_timer))

        # Calculate blended color between two adjacent glow colors
        color_idx = int(self.glow_timer / math.pi) % len(self.glow_colors)
        next_color_idx = (color_idx + 1) % len(self.glow_colors)

        color1 = self.glow_colors[color_idx]
        color2 = self.glow_colors[next_color_idx]

        glow_color = (
            int(color1[0] * (1 - glow_blend) + color2[0] * glow_blend),
            int(color1[1] * (1 - glow_blend) + color2[1] * glow_blend),
            int(color1[2] * (1 - glow_blend) + color2[2] * glow_blend)
        )

        # Draw multiple concentric circles for glow effect
        for i in range(4):
            glow_alpha = 180 - i * 40
            glow_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            pygame.draw.circle(
                glow_surf,
                (*glow_color, glow_alpha),
                self.center,
                self.radius + self.glow_radius_offset + i * 3,
                self.glow_thickness - i * 2
            )
            surface.blit(glow_surf, (0, 0))

        # Draw main boundary circle
        pygame.draw.circle(
            surface,
            self.color,
            self.center,
            self.radius,
            self.thickness
        )


# Bouncing Object Class
class BouncingObject:
    def __init__(self, image_path: str, position: Tuple[float, float],
                 velocity: Tuple[float, float], size: int = 100):
        self.original_image = pygame.image.load(image_path)
        self.original_image = pygame.transform.scale(self.original_image, (size, size))

        # Make image background transparent if it has transparency
        if self.original_image.get_alpha():
            self.image = self.original_image.copy()
        else:
            # Create mask for circular image
            self.image = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 255, 255, 0), (size // 2, size // 2), size // 2)
            self.image.blit(self.original_image, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

        self.size = size
        self.position = list(position)
        self.velocity = list(velocity)
        self.rotation = 0
        self.rotation_speed = random.uniform(-5, 5)
        self.trail = []
        self.max_trail_length = 20
        self.bounce_count = 0
        self.glow_colors = [
            (230, 0, 115, 150),  # Pink with alpha
            (252, 185, 0, 150),  # Gold with alpha
            (64, 224, 208, 150)  # Turquoise with alpha
        ]
        self.current_glow = random.choice(self.glow_colors)

    def update(self, boundaries: List[Boundary]) -> None:
        # Apply gravity
        self.velocity[1] += GRAVITY

        # Store previous position for trail
        self.trail.append(tuple(self.position))
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)

        # Update position
        new_position = [
            self.position[0] + self.velocity[0],
            self.position[1] + self.velocity[1]
        ]

        # Check for collision with each boundary
        for boundary in boundaries:
            if not boundary.is_inside(new_position):
                # Collision detected - calculate bounce
                normal = boundary.get_normal(self.position)

                # Calculate reflection vector
                dot_product = (
                        self.velocity[0] * normal[0] +
                        self.velocity[1] * normal[1]
                )

                self.velocity[0] = self.velocity[0] - 2 * dot_product * normal[0]
                self.velocity[1] = self.velocity[1] - 2 * dot_product * normal[1]

                # Apply dampening
                self.velocity[0] *= BOUNCE_DAMPENING
                self.velocity[1] *= BOUNCE_DAMPENING

                # Add some randomness to make it more interesting
                self.velocity[0] += random.uniform(-2, 2)
                self.velocity[1] += random.uniform(-1, 1)

                # Change rotation on bounce
                self.rotation_speed = random.uniform(-8, 8)

                # Count bounce and change glow color
                self.bounce_count += 1
                if self.bounce_count % 3 == 0:
                    self.current_glow = random.choice(self.glow_colors)

                break

        # Update position
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        # Update rotation
        self.rotation += self.rotation_speed
        if self.rotation >= 360:
            self.rotation -= 360

    def draw(self, surface: pygame.Surface) -> None:
        # Draw trail
        if len(self.trail) > 2:
            points = [(int(x), int(y)) for x, y in self.trail]
            for i in range(len(points) - 1):
                alpha = int(255 * (i / len(points)))
                width = int(self.size * 0.2 * (i / len(points)))
                color_with_alpha = (*self.current_glow[:3], alpha // 3)

                if width > 0:
                    pygame.draw.line(
                        surface,
                        color_with_alpha,
                        points[i],
                        points[i + 1],
                        width
                    )

        # Draw glow
        glow_surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(
            glow_surf,
            self.current_glow,
            (self.size, self.size),
            self.size // 2 + 10
        )
        surface.blit(
            glow_surf,
            (int(self.position[0] - self.size), int(self.position[1] - self.size))
        )

        # Draw rotated image
        rotated_image = pygame.transform.rotate(self.image, self.rotation)
        new_rect = rotated_image.get_rect(
            center=(int(self.position[0]), int(self.position[1]))
        )
        surface.blit(rotated_image, new_rect.topleft)


# Animation Manager Class
class AnimationManager:
    def __init__(self, width: int, height: int, fps: int, title: str = "Bouncing Animation"):
        self.width = width
        self.height = height
        self.fps = fps
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.boundaries = []
        self.objects = []
        self.running = False
        self.recording = False
        self.frame_count = 0
        self.max_frames = fps * 15  # 15 seconds of animation
        self.output_folder = "animation_frames"
        self.bg_color = BG_COLOR

        # Create output folder if recording
        if self.recording and not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def add_boundary(self, boundary: Boundary) -> None:
        self.boundaries.append(boundary)

    def add_object(self, obj: BouncingObject) -> None:
        self.objects.append(obj)

    def handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_r:
                    self.recording = not self.recording
                    print(f"Recording: {self.recording}")
        return True

    def update(self) -> None:
        for obj in self.objects:
            obj.update(self.boundaries)

    def draw(self) -> None:
        # Create background with gradient
        self.screen.fill(self.bg_color)

        # Draw all boundaries
        for boundary in self.boundaries:
            boundary.draw(self.screen)

        # Draw all objects
        for obj in self.objects:
            obj.draw(self.screen)

        # Save frame if recording
        if self.recording:
            pygame.image.save(
                self.screen,
                f"{self.output_folder}/frame_{self.frame_count:04d}.png"
            )
            self.frame_count += 1

            # Stop recording after max frames
            if self.frame_count >= self.max_frames:
                self.recording = False
                print(f"Recording complete. {self.frame_count} frames saved.")

        # Update display
        pygame.display.flip()

    def run(self) -> None:
        self.running = True
        while self.running:
            self.running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)

        pygame.quit()
        sys.exit()


# Function to create a sample animation
def create_bouncing_animation(image_path: str) -> None:
    # Create animation manager
    manager = AnimationManager(WIDTH, HEIGHT, FPS, "Viral Bouncing Animation")

    # Create circular boundary
    boundary = CircleBoundary(
        center=(WIDTH // 2, HEIGHT // 2),
        radius=min(WIDTH, HEIGHT) // 2 - 100,
        color=(255, 255, 255)  # White border
    )
    manager.add_boundary(boundary)

    # Create bouncing objects
    for _ in range(3):  # Add multiple objects for more visual interest
        # Random position inside the boundary
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(0, boundary.radius * 0.7)
        position = (
            boundary.center[0] + math.cos(angle) * distance,
            boundary.center[1] + math.sin(angle) * distance
        )

        # Random initial velocity
        velocity = (
            random.uniform(-MAX_INITIAL_VELOCITY, MAX_INITIAL_VELOCITY),
            random.uniform(-MAX_INITIAL_VELOCITY, MAX_INITIAL_VELOCITY)
        )

        # Random size
        size = random.randint(60, 120)

        # Create object
        obj = BouncingObject(image_path, position, velocity, size)
        manager.add_object(obj)

    # Run animation
    manager.run()


# Example usage
if __name__ == "__main__":
    # Replace with your own image path
    image_path = "emoji.png"  # You can use any image file

    # Check if image exists, otherwise create a simple image
    if not os.path.exists(image_path):
        # Create a simple smiley face image
        img_size = 100
        smiley = pygame.Surface((img_size, img_size), pygame.SRCALPHA)

        # Draw yellow circle
        pygame.draw.circle(smiley, (255, 255, 0), (img_size // 2, img_size // 2), img_size // 2)

        # Draw eyes
        eye_radius = img_size // 10
        pygame.draw.circle(smiley, (0, 0, 0), (img_size // 3, img_size // 3), eye_radius)
        pygame.draw.circle(smiley, (0, 0, 0), (img_size * 2 // 3, img_size // 3), eye_radius)

        # Draw smile
        pygame.draw.arc(
            smiley,
            (0, 0, 0),
            (img_size // 4, img_size // 4, img_size // 2, img_size // 2),
            0,
            math.pi,
            3
        )

        # Save image
        pygame.image.save(smiley, image_path)
        print(f"Created default emoji image: {image_path}")

    create_bouncing_animation(image_path)