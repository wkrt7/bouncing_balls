import math

from pydantic import BaseModel, field_validator, validator


class Vector(BaseModel):
    x: float
    y: float

    def distance(self, other: "Vector"):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def __sub__(self, other):
        return Vector(x=self.x - other.x, y=self.y - other.y)


class Position(Vector):
    x: int | float  # todo make it only float
    y: int | float

    def __add__(self, other):
        if isinstance(other, Velocity):
            return Position(x=int(self.x + other.x), y=int(self.y + other.y))
        if isinstance(other, Position):
            return Position(x=int(self.x + other.x), y=int(self.y + other.y))

    def to_tuple(self):
        return self.x, self.y

    @field_validator("x", mode="before")
    def convert_to_int(cls, value):
        return int(value)

    @field_validator("y", mode="before")
    def convert_to_int_2(cls, value):
        return int(value)


class Velocity(Vector):
    x: int | float
    y: int | float

    @field_validator("x", mode="before")
    def convert_to_int(cls, value):
        return int(value)

    @field_validator("y", mode="before")
    def convert_to_int_2(cls, value):
        return int(value)
