import math
from abc import ABC, abstractmethod

import pygame.draw

from helpers import Position, Vector


class BoundaryProtocol(ABC):
    out_of_boundaries: bool

    @abstractmethod
    def draw(self, screen): ...

    @abstractmethod
    def collision_check(self, new_position): ...

    @abstractmethod
    def get_normal(self, position: Position) -> Vector: ...

    @abstractmethod
    def update(self): ...
