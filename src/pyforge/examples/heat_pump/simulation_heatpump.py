"""
Simple performance calculation for the heat pump.
"""
from pyforge.examples.heat_pump.parameters_heatpump import HEATPUMP_PARAMS

def compute_electrical_input() -> float:
    """
    Returns the electrical power (W) needed to achieve the
    specified heating_capacity at the given COP.
    """
    Q_th = HEATPUMP_PARAMS.heating_capacity.magnitude
    cop = HEATPUMP_PARAMS.cop
    return Q_th / cop

# allow direct execution
if __name__ == "__main__":
    P_el = compute_electrical_input()
    print(f"Electrical input required: {P_el:.2f} W")
