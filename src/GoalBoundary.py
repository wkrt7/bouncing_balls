import pygame

from Boundary import BoundaryProtocol
from helpers import Position, Vector


# Add this to Boundary.py as a new boundary type
class GoalBoundary(BoundaryProtocol):
    def __init__(self, position: Position, width, height, color):
        self.position = position  # Top-left corner
        self.width = width
        self.height = height
        self.color = color
        self.goal_scored = False

    def collision_check(self, position: Position) -> bool:
        # For goal line, we want to detect when objects pass through, not bounce
        return True  # Always return True so objects pass through

    def check_goal(self, ball_position: Position, ball_radius: float) -> bool:
        # Check if the ball center is within the goal area
        if (
            self.position.x <= ball_position.x <= self.position.x + self.width
            and self.position.y <= ball_position.y <= self.position.y + self.height
        ):
            self.goal_scored = True
            return True
        return False

    def get_normal(self, position: Position) -> Vector:
        # This isn't used for physics since balls pass through
        return Vector(x=0, y=0)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.position.x, self.position.y, self.width, self.height), 2)
