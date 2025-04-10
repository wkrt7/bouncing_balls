import os
import sys
from pathlib import Path

import pygame

from bootstrap import BG_COLOR, BOUNDARY_COLOR, HEIGHT, WIDTH
from BouncingObject import BouncingCircle, BouncingObject
from Boundary import BoundaryProtocol
from CircleBoundary import CircleBoundary
from CircleBoundaryWithDoor import CircleBoundaryWithDoor

# from ExitZone import ExitZone
from helpers import Position, Velocity


class AnimationManger:
    def __init__(self, width: int = 800, height: int = 600, fps: int = 60):
        self.running = True
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.init()
        pygame.display.set_caption("title")

        self.clock = pygame.time.Clock()
        self.frame_count = 0
        self.bg_color = BG_COLOR

        self.fps = fps
        self.objects: list[BouncingObject] = []
        self.boundaries: list[BoundaryProtocol] = []

    def add_object(self, object: BouncingObject):
        self.objects.append(object)

    def add_boundary(self, boundary: BoundaryProtocol):
        self.boundaries.append(boundary)

    def update(self):

        for obj in self.objects:
            obj.update(self.boundaries, self.objects)
        for bound in self.boundaries:
            bound.update()
            if bound.out_of_boundaries:
                return False
        return True

    def draw(self):
        self.screen.fill(self.bg_color)

        for boundary in self.boundaries:
            boundary.draw(self.screen)

        for obj in self.objects:
            obj.draw(self.screen)

        pygame.display.flip()

    def handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                return False

        return True

    def _validate_objects(self):
        if len(self.objects) > 0:
            if not all(isinstance(obj, type(self.objects[0])) for obj in self.objects):
                raise TypeError("All objects should be of the same type")

    def _validate(self):
        self._validate_objects()

    def run(self):
        print("Starting...")
        self.running = True
        self._validate()
        while self.running:
            self.running = self.handle_events()
            self.running = self.update()
            self.draw()
            self.clock.tick(self.fps)
            # print("Running")
        print("Ended")
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    anim = AnimationManger(height=HEIGHT, width=WIDTH)
    starting_position = Position(x=WIDTH / 2 + 30, y=HEIGHT / 2)
    radius = 20
    ROOT = Path.cwd()

    # boundary = CircleBoundary(
    #     center=Position(x=WIDTH / 2, y=HEIGHT / 2),
    #     radius=200,
    #     color=BOUNDARY_COLOR,
    #     thicnkess=6,
    # )
    boundary = CircleBoundaryWithDoor(
        center=Position(x=WIDTH / 2, y=HEIGHT / 2),
        radius=200,
        color=BOUNDARY_COLOR,
        thickness=6,
        door_angle_start=90,  # Door starts at 45 degrees (top-right)
        door_angle_size=20,  # Door spans 60 degrees
        rotation_speed=1,
    )
    obj_1 = BouncingCircle(
        position=starting_position, radius=radius, image_path=str(ROOT / "logo.svg"), velocity=Velocity(x=0, y=0)
    )
    obj_2 = BouncingCircle(
        position=Position(x=WIDTH / 2 - 30, y=HEIGHT / 2),
        radius=radius,
        image_path=str(ROOT / "logo.svg"),
        velocity=Velocity(x=0, y=0),
    )
    # Move the window to your second monitor
    # Adjust these values for your monitor setup
    anim.add_object(obj_1)
    anim.add_object(obj_2)
    anim.add_boundary(boundary)

    # anim.add_boundary(exit_zone)
    anim.run()
