from pyforge.note import (
    Citation, DocumentConfig, Figure, Table, Title, display
)
from pyforge.examples.heat_pump.parameters_heatpump import HEATPUMP_PARAMS
from pyforge.examples.heat_pump.systems_heatpump import heat_pump
from pyforge.examples.heat_pump.simulation_heatpump import compute_electrical_input

import pandas as pd
from pathlib import Path

# 1. Document metadata
config = DocumentConfig(
    title="Heat Pump Design Report",
    author="Charles Azam",
    date="2025-05-18"
)
display(config)

# 2. Title
display(Title("# Heat Pump System Design"))

# 3. Parameters table
df_params = pd.DataFrame([
    {"Parameter": "Heating Capacity", "Value": f"{HEATPUMP_PARAMS.heating_capacity}"},
    {"Parameter": "COP",              "Value": HEATPUMP_PARAMS.cop},
    {"Parameter": "Evaporator Temp",  "Value": f"{HEATPUMP_PARAMS.evaporator_temp}"},
    {"Parameter": "Condenser Temp",   "Value": f"{HEATPUMP_PARAMS.condenser_temp} "},
    {"Parameter": "Flow Rate",        "Value": f"{HEATPUMP_PARAMS.flow_rate} "},
    {"Parameter": "Design Life",      "Value": f"{HEATPUMP_PARAMS.design_life} years"},
])
display(Table(df_params, "Core design parameters", "tbl-params"))

# 4. System description & requirements
display("## System Overview")
display(heat_pump.display())

# 5. Simulation results
P_el = compute_electrical_input()
df_perf = pd.DataFrame([
    {"Metric": "Electrical Input", "Value": f"{P_el:.2f} W"},
    {"Metric": "Implied Power Ratio", "Value": f"{P_el/HEATPUMP_PARAMS.heating_capacity.magnitude:.3f}"}
])
display(Table(df_perf, "Performance estimates", "tbl-perf"))

# 6. Conclusion
display(
    Title("# Conclusion"),
    "This report summarises the basic design parameters and "
    "simulated performance of our heat pump system. "
    "Further iterations could refine transient behaviour and "
    "optimize the refrigerant loop design."
)
