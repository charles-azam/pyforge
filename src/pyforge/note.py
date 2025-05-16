from abc import ABC
from pathlib import Path

from beartype import beartype
import pandas as pd
import streamlit as st


class MultiDisplayer(ABC):
    pass

@beartype
class Figure:
    def __init__(self, path: Path, caption: str, label: str | None = None):
        pass


@beartype
class Table:
    def __init__(self, data: pd.DataFrame, caption: str, label: str | None = None):
        pass


@beartype
class Citation:
    def __init__(self, id: str, text: str | None = None): ...

    pass


@beartype
class Reference:
    def __init__(self, label: str, text: str | None = None): ...


@beartype
class Title:
    def __init__(self, text: str, label: str | None = None):
        pass

    pass


@beartype
def display(
    *content: str | MultiDisplayer,
    confidential: bool = False,
):
    pass
