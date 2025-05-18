import pytest
from pint import Quantity, UnitRegistry

# Replace `pyforge_models` with the actual module name where your classes live
from pyforge.systems import (
    Parameters,
    Requirement,
    Function,
    System,
    convert_quantity_to_str,
    UREG,
)

class DummyParams(Parameters):
    """A simple Parameters subclass for testing."""
    length: Quantity = UREG.Quantity(2, "m")
    count: int = 5

def test_convert_quantity_to_str_pretty():
    """Quantity formatting uses Pint's pretty format."""
    q = UREG.Quantity(5, "meter") / UREG.Quantity(2, "second")
    s = convert_quantity_to_str(q)
    # Expect something like "2.5 m/s"
    assert "m" in s
    assert "/" in s

def test_parameters_display_table():
    """Parameters.display() renders a markdown table of fields."""
    params = DummyParams()
    md = params.display().splitlines()
    # Header row should be present
    assert md[0] == "| Parameter | Value |"
    assert md[1] == "| --- | --- |"
    # One row for 'length' and one for 'count'
    assert any("length" in line and "2" in line for line in md)
    assert any("count" in line and "5" in line for line in md)

def test_requirement_display():
    """Requirement.display() returns a markdown bullet."""
    req = Requirement(name="Req1", description="Must do X")
    out = req.display()
    assert out == "- **Req1**: Must do X"

def test_function_display_without_params():
    """Function.display() handles absence of parameters."""
    func = Function(name="FuncA", description="Does A")
    md = func.display()
    assert "### Function: FuncA" in md
    assert "Does A" in md
    assert "Parameters" not in md

def test_function_display_with_params():
    """Function.display() includes parameters table if present."""
    params = DummyParams()
    func = Function(name="FuncB", description="Does B", parameters=params)
    md = func.display().splitlines()
    # Header
    assert md[0] == "### Function: FuncB"
    # Description line
    assert "Does B" in md[1]
    # Parameters section appears
    assert any("Parameter | Value" in line for line in md)

def test_system_display_full():
    """System.display() renders all sections: name, desc, params, reqs, funcs, children."""
    # Set up child system
    child = System(name="ChildSys", description="Child system desc")
    # Parent with everything
    parent = System(
        name="ParentSys",
        description="Parent system desc",
        parameters=DummyParams(),
        requirements=[Requirement(name="R1", description="D1")],
        functions=[Function(name="F1", description="DF1")],
        children=[child],
    )
    md = parent.display().splitlines()
    # Title
    assert md[0] == "# System: ParentSys"
    # Description
    assert "Parent system desc" in md[1]
    # Parameters header
    assert "## Parameters" in md
    # Requirements header and item
    assert "## Requirements" in md
    assert any("**R1**" in line for line in md)
    # Functions header and item
    assert "## Functions" in md
    assert any("### Function: F1" in line for line in md)
    # Subsystems header and child's title
    assert "## Subsystems" in md
    assert any("# System: ChildSys" in line for line in md)
