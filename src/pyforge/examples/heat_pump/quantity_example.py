from pint import Quantity
from pyforge import Parameters, System, Requirement, UREG

width = Quantity(2, "m")
height = Quantity(3, "m")
area = width * height
print(f"Area: {area}")
# Area: 6 m²

# Example of conversion
area_cm2 = area.to("cm^2")
area_cm2_magnitude = area_cm2.magnitude
assert area_cm2_magnitude == 6 * 100 * 100
area_cm2_units = str(area.units)
assert str(area.units) == "meter ** 2"