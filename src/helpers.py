from pydantic import BaseModel, validator, field_validator


class Position(BaseModel):
    x : int|float  # todo make it only float
    y : int|float

    def __add__(self, other):
        if isinstance(other, Velocity):
            return Position(x=int(self.x + other.x), y=int(self.y + other.y))
        if isinstance(other, Position):
            return Position(x=int(self.x + other.x), y=int(self.y + other.y))

    def to_tuple(self):
        return self.x, self.y

    @field_validator("x",mode="before")
    def convert_to_int(cls, value):
        return int(value)

    @field_validator("y",mode="before")
    def convert_to_int_2(cls, value):
        return int(value)

class Velocity(BaseModel):
    x:int
    y:int
