from abc import ABC,abstractmethod
import random

from Boundary import BoundaryProtocol
from bootstrap import GRAVITY
import pygame.draw

from bootstrap import OBJECT_COLOR

from helpers import Position, Velocity


class BouncingObject(ABC):
    @abstractmethod
    def update(self, boundaries:list[BoundaryProtocol]):
        ...

    @abstractmethod
    def draw(self, screen):
        ...


class BouncingCircle(BouncingObject):
    def __init__(self, image_path, radius, position: Position, velocity: Velocity):
        self.image_path = image_path
        self.radius = radius
        self.position = position
        self.velocity = velocity

    def update(self, boundaries:list[BoundaryProtocol]):
        self.velocity.y += GRAVITY
        new_position = self.position + self.velocity
        for boundary in boundaries:
            if not boundary.collision_check(new_position):
                # Collision detected - calculate bounce
                normal_position = boundary.get_normal(self.position)

                # Calculate reflection vector
                dot_product = (
                        self.velocity.x * normal_position.x +
                        self.velocity.y * normal_position.y
                )

                self.velocity.x = self.velocity.x - 2 * dot_product * normal_position.x
                self.velocity.y = self.velocity.y - 2 * dot_product * normal_position.y

                # Apply dampening
                # self.velocity[0] *= BOUNCE_DAMPENING
                # self.velocity[1] *= BOUNCE_DAMPENING

                # Add some randomness to make it more interesting
                # self.velocity.x += random.uniform(0, 2)
                # self.velocity.y += random.uniform(0, 1)

                # Change rotation on bounce
                # self.rotation_speed = random.uniform(-8, 8)

                # Count bounce and change glow color
                # self.bounce_count += 1
                # if self.bounce_count % 3 == 0:
                #     self.current_glow = random.choice(self.glow_colors)

                break

        self.position += self.velocity


        # self.position.x += self.position.x_speed
        # self.position.y += self.position.y_speed
        # if self.position.x < 0 or self.position.x > 800:
        #     self.position.x_speed = -self.position.x_speed
        # if self.position.y < 0 or self.position.y > 600:
        #     self.position.y_speed = -self.position.y_speed

    def draw(self, screen):
        # Load the image and draw it at the current position
        pygame.draw.circle(screen, OBJECT_COLOR, (self.position.x,self.position.y), self.radius)