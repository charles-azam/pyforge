from pyforge import System, Requirement
from pyforge.examples.heat_pump.parameters_heatpump import HEATPUMP_PARAMS

# Root “Heat Pump” system
heat_pump = System(
    name="Heat Pump System",
    description=(
        f"{HEATPUMP_PARAMS.heating_capacity.magnitude}{HEATPUMP_PARAMS.heating_capacity.units} "
        f"heat output at COP {HEATPUMP_PARAMS.cop}"
    ),
    requirements=[
        Requirement(
            name="Thermal Capacity",
            description=(
                f"Deliver {HEATPUMP_PARAMS.heating_capacity.magnitude}"
                f"{HEATPUMP_PARAMS.heating_capacity.units} at "
                f"{HEATPUMP_PARAMS.condenser_temp.magnitude}"
                f"{HEATPUMP_PARAMS.condenser_temp.units}."
            )
        ),
        Requirement(
            name="Minimum Efficiency",
            description=(
                f"COP ≥ {HEATPUMP_PARAMS.cop} under rated conditions."
            )
        )
    ]
)
