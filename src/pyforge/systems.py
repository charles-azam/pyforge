from __future__ import annotations
from pydantic import BaseModel
from pint import Quantity, UnitRegistry

# Initialize Pint registry
UREG = UnitRegistry()

def convert_quantity_to_str(quantity: Quantity) -> str:
    """Convert a Pint Quantity to a human-friendly string."""
    try:
        # ‘~P’ = pretty + abbreviated units, e.g. “5.0 m/s”
        return format(quantity, "~P")
    except Exception:
        return str(quantity)

class Parameters(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    def display(self) -> str:
        """Return a markdown table of all parameters and their values."""
        try:
            data = self.model_dump()
            if not data:
                return ""
            lines = ["| Parameter | Value |", "| --- | --- |"]
            for key, val in data.items():
                text = convert_quantity_to_str(val) if isinstance(val, Quantity) else str(val)
                lines.append(f"| {key} | {text} |")
            return "\n".join(lines)
        except Exception:
            return str(self)

class Requirement(BaseModel):
    name: str = ""
    description: str = ""

    def display(self) -> str:
        """Return a markdown bullet point for this requirement."""
        return f"- **{self.name}**: {self.description}"

class Function(BaseModel):
    name: str = ""
    description: str = ""
    parameters: Parameters | None = None

    def display(self) -> str:
        """Return a markdown section describing this function."""
        header = f"### Function: {self.name}"
        desc = self.description or ""
        param_md = ("\n**Parameters:**\n" + self.parameters.display()) if self.parameters else ""
        return f"{header}\n\n{desc}{param_md}"

class System(BaseModel):
    name: str = ""
    description: str = ""
    requirements: list[Requirement] | None = None
    functions: list[Function] | None = None
    children: list[System] | None = None
    parameters: Parameters | None = None  # fixed typo
    cost: float | None = None

    def add_child(self, system: System):
        """Add a subsystem to the children list."""
        if self.children is None:
            self.children = [system]
        else:
            self.children.append(system)

    def display(self) -> str:
        """Return a markdown representation of this system."""
        md: list[str] = [f"# System: {self.name}", "", self.description or ""]

        if self.parameters:
            md.append("\n## Parameters")
            md.append(self.parameters.display())

        if self.requirements:
            md.append("\n## Requirements")
            for req in self.requirements:
                md.append(req.display())

        if self.functions:
            md.append("\n## Functions")
            for func in self.functions:
                md.append(func.display())

        if self.children:
            md.append("\n## Subsystems")
            for child in self.children:
                md.append(child.display())

        return "\n".join(md)
