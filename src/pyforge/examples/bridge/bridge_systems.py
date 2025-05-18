from pint import Quantity
from pyforge import Parameters, System, Requirement, UREG

# Example of using PyForge
class BridgeParameter(Parameters):
    length: Quantity = Quantity(120, "m")
    height: Quantity = Quantity(15, "m")
    width: Quantity = Quantity(12, "m")
    deck_thickness: Quantity = Quantity(0.25, "m")
    design_life: int = 40

BRIDGE_PARAMS = BridgeParameter()

root_system = System(name = "Bridge")

structural_system = System(
    name="Structural System",
    description=(
        f"Spans {BRIDGE_PARAMS.length} at "
        f"{BRIDGE_PARAMS.height} high, "
        f"with a {BRIDGE_PARAMS.deck_thickness}-thick deck."
    ),
    requirements=[
        Requirement(
            name="Load Capacity",
            description=(
                f"Must safely carry traffic for {BRIDGE_PARAMS.design_life} years "
                f"across a {BRIDGE_PARAMS.width} wide deck."
            )
        ),
    ]
)

safety_system = System(
    name="Safety System",
    description=(
        f"Provides railings, walkways along the {BRIDGE_PARAMS.length} span."
    ),
    requirements=[
        Requirement(
            name="Guardrail Height",
            description=(
                f"Minimum 1.2 m tall railings at {BRIDGE_PARAMS.height.magnitude}"
                f"{BRIDGE_PARAMS.height.units} above ground."
            )
        )
    ]
)
# systems form a tree
root_system.add_child(safety_system)
root_system.add_child(structural_system)