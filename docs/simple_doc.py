from pathlib import Path

import pandas as pd

from pyforge.note import (Citation, DocumentConfig, Figure,
                          Reference, Table, Title, display)
from pyforge.common import ROOT_PYFORGE_DIR

# Document configuration
config = DocumentConfig(
    title="Example PyForge Document", author="PyForge User", date="2025-05-16"
)
display(config)

# Create a sample dataframe for demonstration
df = pd.DataFrame(
    {
        "Name": ["Alice", "Bob", "Charlie"],
        "Age": [25, 30, 35],
        "City": ["New York", "London", "Paris"],
    }
)

display("""
# Introduction
This is an example document created with PyForge. It demonstrates how to use various components like titles, figures, tables, and citations.

## Pyforge Overview
PyForge allows you to write documents in Python with a syntax similar to markdown. You can include regular markdown text as strings, and use special classes for figures, tables, and other elements.
  
## Create sample figure      
        """)

display(
    Figure(ROOT_PYFORGE_DIR/"logo.png", "Sample figure", "figure-sample")
)

display(
Table(df, "Sample data table", "table-sample"),
"You can reference the table above using a Reference object.",
Reference("table-sample", "Table 1"),
"You can also include citations like this:",
Citation("smith2023", "Smith et al. (2023)"),
Title("# Conclusion"),
"This example demonstrates the basic functionality of PyForge for document creation.",
)
