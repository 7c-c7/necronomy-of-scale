import dataclasses


@dataclasses.dataclass
class Position:
    x: int = 0
    y: int = 0
    z: int = 0

    def __str__(self):
        return f"@{dataclasses.astuple(self)}"


@dataclasses.dataclass(eq=False)
class Movement:
    speed: int  # per turn (6 seconds), in feet

    def __str__(self):
        return f"{self.name} {self.speed} ft."

    @property
    def name(self):
        return type(self).__name__

    def __eq__(self, other):
        return id(self) == id(other)

    def __hash__(self):
        return id(self)


# Movement types
class Walk(Movement):
    pass


class Fly(Movement):
    pass


class Swim(Movement):
    pass


class Burrow(Movement):
    pass


class Climb(Movement):
    pass


class Hover(Movement):
    pass


class Crawl(Movement):
    pass
