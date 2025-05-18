# PyForge

[PyForge](https://github.com/charles-azam/pyforge) is a lightweight Python framework for writing technical documentation and system-engineering models as code. Its core philosophy is to maintain a single source of truth—your Python scripts—while enabling multiple output formats (Markdown, HTML, Streamlit, etc.).

---

## Key Features

- **Code-first documents**  
  Write your docs in Python, mixing Markdown strings with programmatic content.
- **System-engineering primitives**  
  Define parameters, hierarchical systems, requirements, and simulations in a structured API.
- **Minimal dependencies**  
  Pure Python + a few small libraries—no heavy toolchain to install.

---

## Installation

**Using `uv`** (recommended for this repo):

```bash
git clone https://github.com/charles-azam/pyforge.git
cd pyforge
uv sync
````

**Or via `pip`:**

```bash
git clone https://github.com/charles-azam/pyforge.git
cd pyforge
pip install -e .
```

---

## Project Structure

Organize your files by purpose. PyForge will discover and import them in this order:

* **`parameters_*.py`**
  Define engineering parameters (with units).
* **`systems_*.py`**
  Build hierarchical system definitions and attach requirements.
* **`simulation_*.py`**
  Implement computations, simplified physics models, or performance estimates.
* **`tools_*.py`**
  Helpers and domain-specific utilities.
* **`design.py`**
  Main entry point. Imports all other modules and orchestrates the design.

!!! tip
    Any `display()` statements in your modules will be captured and fed into the next iteration of the pipeline. Don’t wrap them in an `if __name__ == "__main__"` guard.

---

## Usage: Defining Systems and parameters

```python
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
```


```python
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
```

---

## Usage: Writing Documents

Leverage Python logic alongside Markdown-style content. PyForge lets you embed tables, figures, citations, and more.

```python
from pathlib import Path
import pandas as pd
from pyforge.note import (
    Citation, DocumentConfig, Figure, Reference, Table, Title, display
)

# Configure document metadata
config = DocumentConfig(
    title="Example PyForge Document",
    author="Your Name",
    date="2025-05-16"
)
display(config)

# Sample DataFrame
df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "City": ["New York", "London", "Paris"]
})

display(
    "# Introduction\n"
    "This document demonstrates PyForge’s capabilities.\n\n"
    "## PyForge Overview\n"
    "Write docs in Python with Markdown strings and special classes."
)

display(
    Table(df, "Sample data table", "tbl-sample"),
    "Reference the table above:", Reference("tbl-sample", "Table 1"),
    "Include citations:", Citation("smith2023", "Smith et al. (2023)"),
    Title("# Conclusion"),
    "PyForge makes it easy to generate and version technical documents."
)
```

---

## CLI & Display Modes

* **Markdown export**

  ```bash
  pyforge markdown design.py output.md
  ```
* **Interactive preview**

  ```bash
  pyforge view design.py
  # (uses Streamlit under the hood)
  ```

See the `docs/` folder for example scripts:

* `simple_doc.py` — basic usage
* `complex_doc.py` — figures, tables, and citations

---

## Philosophy

PyForge is intentionally minimalist. It gives you just enough structure to programmatically create and version technical documents—without locking you into a heavyweight toolchain.

---

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.

