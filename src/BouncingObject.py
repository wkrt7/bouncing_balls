import random
import uuid
from abc import ABC, abstractmethod
from typing import Protocol

import pygame.draw

from bootstrap import BOUNCE_DAMPENING, GRAVITY, OBJECT_COLOR
from Boundary import BoundaryProtocol
from helpers import Position, Velocity


class BouncingObject(Protocol):
    object_id: uuid.UUID
    position: Position
    velocity: Velocity
    initial_position: Position

    @abstractmethod
    def update(self, boundaries: list[BoundaryProtocol], objects: list["BouncingObject"]): ...

    @abstractmethod
    def draw(self, screen): ...


class BouncingCircle(BouncingObject):
    def __init__(self, image_path, radius, position: Position, velocity: Velocity):
        self.radius = radius
        self.position = position
        self.velocity = velocity
        self.object_id = uuid.uuid4()
        self.initial_position = position

    def update(self, boundaries: list[BoundaryProtocol], objects: list["BouncingCircle"]):
        self.velocity.y += GRAVITY
        new_position = self.position + self.velocity
        for boundary in boundaries:
            if not boundary.collision_check(new_position):
                # Collision detected - calculate bounce
                normal_position = boundary.get_normal(self.position)

                # Calculate reflection vector
                dot_product = self.velocity.x * normal_position.x + self.velocity.y * normal_position.y

                self.velocity.x = self.velocity.x - 2 * dot_product * normal_position.x
                self.velocity.y = self.velocity.y - 2 * dot_product * normal_position.y
                # Apply dampening
                self.velocity.x *= BOUNCE_DAMPENING
                self.velocity.y *= BOUNCE_DAMPENING

                # Add some randomness to make it more interesting
                self.velocity.x += random.uniform(-2, 2)
                self.velocity.y += random.uniform(-1, 1)

                # Change rotation on bounce
                # self.rotation_speed = random.uniform(-8, 8)

                # Count bounce and change glow color
                # self.bounce_count += 1
                # if self.bounce_count % 3 == 0:
                #     self.current_glow = random.choice(self.glow_colors)

                break
        for object in objects:
            if self.object_id != object.object_id:
                # distance between this object and object is smaller than sum of radiuses then bounce
                if self.position.distance(object.position) < self.radius + object.radius:
                    delta_pos = self.position - object.position
                    delta_vel = self.velocity - object.velocity
                    distance_squared = delta_pos.x**2 + delta_pos.y**2
                    if distance_squared > 0:  # Avoid division by zero
                        dot_product = (delta_vel.x * delta_pos.x + delta_vel.y * delta_pos.y) / distance_squared
                        self.velocity.x -= dot_product * delta_pos.x
                        self.velocity.y -= dot_product * delta_pos.y
                        object.velocity.x += dot_product * delta_pos.x
                        object.velocity.y += dot_product * delta_pos.y
        self.position += self.velocity

        # self.position.x += self.position.x_speed
        # self.position.y += self.position.y_speed
        # if self.position.x < 0 or self.position.x > 800:
        #     self.position.x_speed = -self.position.x_speed
        # if self.position.y < 0 or self.position.y > 600:
        #     self.position.y_speed = -self.position.y_speed

    def draw(self, screen):
        # Load the image and draw it at the current position
        pygame.draw.circle(screen, OBJECT_COLOR, (self.position.x, self.position.y), self.radius)
