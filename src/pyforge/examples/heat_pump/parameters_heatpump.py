from pyforge import Parameters, Quantity

class HeatPumpParameters(Parameters):
    """Define all the key parameters for our heat pump."""
    heating_capacity: Quantity    = Quantity(10000, "W")   # thermal output
    cop: float                    = 4.0                    # coefficient of performance
    evaporator_temp: Quantity     = Quantity(-5, "°C")
    condenser_temp: Quantity      = Quantity(35, "°C")
    flow_rate: Quantity           = Quantity(0.05, "kg/s")
    design_life: int              = 20                     # years

# single source of truth
HEATPUMP_PARAMS = HeatPumpParameters()
