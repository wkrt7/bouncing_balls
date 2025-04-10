import sys

import Boundary
from BouncingObject import BouncingObject, BouncingCircle
from helpers import Position, Velocity
from pathlib import Path
import pygame

from bootstrap import BG_COLOR, HEIGHT, WIDTH, BOUNDARY_COLOR


class AnimationManger:
    def __init__(self, width:int=800, height:int=600, fps:int=60):
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
        self.objects :list[BouncingObject]= []
        self.boundaries:list[Boundary] = []

    def add_object(self, object:BouncingObject):
        self.objects.append(object)

    def add_boundary(self, boundary:Boundary):
        self.boundaries.append(boundary)

    def update(self):
        for obj in self.objects:
            obj.update(self.boundaries)

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
        return True

    def run(self):
        print("Starting...")
        self.running = True
        while self.running:
            self.running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)
            # print("Running")
        print("Ended")
        pygame.quit()
        sys.exit()


if __name__ =="__main__":
    anim = AnimationManger(height=HEIGHT, width=WIDTH)
    starting_position = Position(x=WIDTH/2 +30, y=HEIGHT/2)

    radius = 20
    ROOT = Path.cwd()

    boundary = Boundary.CircleBoundary(center=Position(x= WIDTH/2, y=HEIGHT/2), radius=200, color=BOUNDARY_COLOR, thicnkess=6)
    obj_1 = BouncingCircle(position=starting_position, radius=radius, image_path=str(ROOT/"logo.svg"),velocity=Velocity(x=0,y=0))

    anim.add_object(obj_1)
    anim.add_boundary(boundary)
    anim.run()


