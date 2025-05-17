from __future__ import annotations
from pydantic import BaseModel
from pint import Quantity, UnitRegistry


class Parameters(BaseModel):
    class Config:
        arbitrary_types_allowed = True


class Requirement(BaseModel):
    name: str = ""
    description: str = ""


class System(BaseModel):
    name: str = ""
    description: str = ""
    requirements: list[Requirement] | None = None
    children: list[System] | None = None

    def add_child(self, system: System):
        if self.children is None:
            self.children = [system]

        else:
            self.children.append(system)


UREG = UnitRegistry()
