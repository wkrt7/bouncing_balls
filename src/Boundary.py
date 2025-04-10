import math
from abc import ABC, abstractmethod

import pygame.draw

from helpers import Position, Vector


class BoundaryProtocol(ABC):
    @abstractmethod
    def draw(self, screen): ...

    @abstractmethod
    def collision_check(self, new_position): ...

    @abstractmethod
    def get_normal(self, position: Position) -> Vector: ...


class CircleBoundary(BoundaryProtocol):
    def __init__(self, center: Position, radius, color, thicnkess):
        self.center = center
        self.radius = radius
        self.color = color
        self.thickness = thicnkess

    def check_collision(self, object) -> bool: ...

    def collision_check(self, position: Position) -> bool:
        dx = position.x - self.center.x
        dy = position.y - self.center.y
        distance_squared = dx * dx + dy * dy
        return distance_squared < (self.radius - 15) ** 2  # 30px buffer for object size

    def get_normal(self, position: Position) -> Vector:
        dx = position.x - self.center.x
        dy = position.y - self.center.y

        distance = math.sqrt(dx * dx + dy * dy)

        if distance == 0:
            return Position(x=0, y=-1)  # Default normal if at center
        return Vector(x=dx / distance, y=dy / distance)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.center.to_tuple(), self.radius, self.thickness)
