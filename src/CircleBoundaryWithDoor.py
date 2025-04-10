import math

import pygame

from Boundary import BoundaryProtocol
from helpers import Position, Vector


class CircleBoundaryWithDoor(BoundaryProtocol):
    def __init__(self, center: Position, radius, color, thickness, door_angle_start, door_angle_size, rotation_speed):
        self.center = center
        self.radius = radius
        self.color = color
        self.thickness = thickness
        # Door parameters (in degrees)
        self.door_angle_start = door_angle_start  # Where the door starts (0 = right, 90 = bottom, etc.)
        self.door_angle_size = door_angle_size  # Size of the door opening in degrees
        self.rotation_speed = rotation_speed  # How fast the door rotates (degrees per frame)
        self.debug = True
        self.out_of_boundaries = False

    def _is_in_door_angle(self, angle_degrees):
        """Check if the given angle is within the door opening"""
        # Normalize angles to 0-360 range
        door_start = self.door_angle_start % 360
        door_end = (door_start + self.door_angle_size) % 360
        angle = angle_degrees % 360

        # Handle the case where the door crosses the 0/360 boundary
        if door_start <= door_end:
            return door_start <= angle <= door_end
        else:
            return angle >= door_start or angle <= door_end

    def collision_check(self, position: Position) -> bool:
        dx = position.x - self.center.x
        dy = position.y - self.center.y
        distance_squared = dx * dx + dy * dy

        # Check if the position is near the boundary
        if not ((self.radius - 25) ** 2 <= distance_squared <= (self.radius + 5) ** 2):
            return True  # Position is either well inside or well outside the circle

        # Calculate the angle in degrees
        angle_radians = math.atan2(dy, dx)
        angle_degrees = math.degrees(angle_radians) % 360
        angle_degrees = 360 - angle_degrees
        # If the position is within the door angle, allow it to pass through
        if self._is_in_door_angle(angle_degrees):
            self.out_of_boundaries = True
            return True  # No collision in the door area

        # Otherwise, treat it as a collision if near the boundary
        return distance_squared < (self.radius - 15) ** 2

    def get_normal(self, position: Position) -> Vector:
        dx = position.x - self.center.x
        dy = position.y - self.center.y

        distance = math.sqrt(dx * dx + dy * dy)

        if distance == 0:
            return Position(x=0, y=-1)  # Default normal if at center
        return Vector(x=dx / distance, y=dy / distance)

    def draw(self, screen):
        # Draw the circle as an arc, leaving a gap for the door
        door_start_radians = math.radians(self.door_angle_start)
        door_end_radians = math.radians((self.door_angle_start + self.door_angle_size) % 360)

        # Draw the circle in two parts to create the door opening
        # Convert to pygame's angle system (counterclockwise from positive x-axis, in degrees)
        pygame.draw.arc(
            screen,
            self.color,
            (self.center.x - self.radius, self.center.y - self.radius, self.radius * 2, self.radius * 2),
            door_end_radians,
            door_start_radians,
            self.thickness,
        )

        if self.debug:
            pygame_deg = 360 - self.door_angle_start
            door_start_rad = math.radians(pygame_deg)
            door_end_rad = math.radians((pygame_deg - self.door_angle_size) % 360)

            # Calculate points on the boundary for the door start and end
            start_x = self.center.x + self.radius * math.cos(door_start_rad)
            start_y = self.center.y + self.radius * math.sin(door_start_rad)
            end_x = self.center.x + self.radius * math.cos(door_end_rad)
            end_y = self.center.y + self.radius * math.sin(door_end_rad)

            # Draw lines from center to door edges
            pygame.draw.line(screen, (255, 0, 0), self.center.to_tuple(), (start_x, start_y), 2)
            pygame.draw.line(screen, (0, 255, 0), self.center.to_tuple(), (end_x, end_y), 2)

    def update(self):
        self.door_angle_start = (self.door_angle_start - self.rotation_speed) % 360
