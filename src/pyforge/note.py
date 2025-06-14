import os
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Any, List, Optional

import pandas as pd
import streamlit as st

from pyforge.common import get_logger

logger = get_logger(__name__)


class DisplayMode(Enum):
    """
    Enum for display modes.
    """

    MARKDOWN = "markdown"
    STREAMLIT = "streamlit"
    PYTHON = "python"


@dataclass
class _DisplayConfig:
    mode: DisplayMode
    output_path: Path | None = None


OUTPUT_MARKDOWN_PATH = "OUTPUT_MARKDOWN_PATH"


def set_markdown_display_mode(output_path: Path):
    """
    Set the display mode to markdown and specify the output path.

    Args:
        output_path: Path to write markdown output to
    """
    os.environ[OUTPUT_MARKDOWN_PATH] = str(output_path)
    logger.info(f"Markdown display mode set with output path: {output_path}")


def unset_markdown_display_mode():
    os.environ.pop(OUTPUT_MARKDOWN_PATH, None)


def is_run_by_streamlit() -> bool:
    try:
        import streamlit as st
    except ImportError:
        return False
    return st.runtime.exists()


def run_file_with_streamlit(filepath: Path, arguments: list[str] | None = None):
    # Credits to https://discuss.streamlit.io/t/how-can-i-invoke-streamlit-from-within-python-code/6612/6
    arguments = ["streamlit", "run", str(filepath)] + (arguments or [])
    sys.argv = arguments
    from streamlit.web import cli as stcli

    sys.exit(stcli.main())


@lru_cache
def get_display_config() -> _DisplayConfig:
    """
    Get the current display configuration.

    Returns:
        _DisplayConfig: Current display configuration
    """

    if os.getenv(OUTPUT_MARKDOWN_PATH):
        output_path = Path(os.getenv(OUTPUT_MARKDOWN_PATH))
        if not output_path.exists():
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.touch()
        return _DisplayConfig(mode=DisplayMode.MARKDOWN, output_path=output_path)

    elif st.runtime.exists():
        return _DisplayConfig(mode=DisplayMode.STREAMLIT)

    else:
        # Default to Python mode if no other mode is set
        return _DisplayConfig(mode=DisplayMode.PYTHON)


class MultiDisplayer(ABC):

    def display(self, mode: DisplayMode):
        """
        Displays the content in the specified mode.
        """
        if mode == DisplayMode.MARKDOWN:
            return self.display_markdown()
        elif mode == DisplayMode.STREAMLIT:
            return self.display_streamlit()
        else:
            raise ValueError(f"Unsupported display mode: {mode}")

    @abstractmethod
    def display_markdown(self) -> str:
        """Return markdown representation"""
        pass

    @abstractmethod
    def display_streamlit(self) -> None:
        """Display in streamlit"""
        pass


class DocumentConfig(MultiDisplayer):
    def __init__(
        self,
        title: str,
        author: str,
        date: str | None = None,
        bib_path: Path | None = None,
    ):
        self.title = title
        self.author = author
        self.date = date
        self.bib_path = bib_path

    def display_markdown(self) -> str:
        """
        Return the markdown metadata representation of the document configuration.
        """
        metadata = [
            "---",
            f"title: {self.title}",
            f"author: {self.author}",
            f"date: {self.date}" if self.date else "",
            f"bibliography: {self.bib_path}" if self.bib_path else "",
            "---",
            "\n"
        ]
        return "\n".join(metadata)

    def display_streamlit(self) -> None:
        """
        Display the document configuration in Streamlit.
        """
        st.markdown(f"# {self.title}")
        st.markdown(f"**Author:** {self.author}")
        if self.date:
            st.markdown(f"**Date:** {self.date}")
        if self.bib_path:
            st.markdown(f"**Bibliography:** {self.bib_path}")


class Figure(MultiDisplayer):
    def __init__(self, path: Path, caption: str, label: str | None = None):
        self.path = path
        self.caption = caption
        self.label = label

    @classmethod
    def from_matplotlib(cls, fig, filename: str, caption: str, label: str | None = None, dpi: int = 300, bbox_inches: str = "tight") -> "Figure":
        """
        Create a Figure instance from a matplotlib figure.
        
        Args:
            fig: matplotlib figure object
            filename: name of the file to save the figure as
            caption: caption for the figure
            label: optional label for referencing the figure
            dpi: dots per inch for the saved figure
            bbox_inches: how to handle the figure's bounding box
            
        Returns:
            Figure instance
        """
        import matplotlib.pyplot as plt
        
        # Get the output path from environment
        output_path = Path(os.environ.get(OUTPUT_MARKDOWN_PATH, Path.cwd()))
        if not output_path:
            raise ValueError("No markdown output path set. Call set_markdown_display_mode first.")
            
        # Create figures directory relative to the markdown output
        figures_dir = output_path.parent / "figures"
        figures_dir.mkdir(exist_ok=True)
        
        # Save the figure
        filepath = figures_dir / filename
        fig.savefig(filepath, dpi=dpi, bbox_inches=bbox_inches)
        plt.close(fig)
        
        return cls(filepath, caption, label)

    def display_markdown(self) -> str:
        label_text = f"{{#{self.label}}}" if self.label else ""
        relative_path = self.path.relative_to(Path(os.environ[OUTPUT_MARKDOWN_PATH]).parent)
        return f"![{self.caption}]({relative_path}){label_text}"

    def display_streamlit(self) -> None:
        st.image(str(self.path), caption=self.caption)


class Table(MultiDisplayer):
    def __init__(self, data: pd.DataFrame, caption: str, label: str | None = None):
        self.data = data
        self.caption = caption
        self.label = label

    def display_markdown(self) -> str:
        md_table = self.data.to_markdown(index=False)
        label_text = f"{{#{self.label}}}" if self.label else ""
        return f"{md_table}\n\n{self.caption}{label_text}"

    def display_streamlit(self) -> None:
        st.caption(self.caption)
        st.dataframe(self.data)


class Citation(MultiDisplayer):
    def __init__(self, id: str, text: str | None = None):
        self.id = id
        self.text = text

    def display_markdown(self) -> str:
        return f"[@{self.id}]"

    def display_streamlit(self) -> None:
        display_text = self.text if self.text else f"[{self.id}]"
        st.text(display_text)


class Reference(MultiDisplayer):
    def __init__(self, label: str, text: str | None = None):
        self.label = label
        self.text = text

    def display_markdown(self) -> str:
        return f"[@{self.label}]"

    def display_streamlit(self) -> None:
        display_text = self.text if self.text else f"[ref:{self.label}]"
        st.text(display_text)


class Title(MultiDisplayer):
    def __init__(self, text: str, label: str | None = None):
        self.text = text
        self.label = label

    @property
    def level(self) -> int:
        """
        Determine the level of the title based on the number of '#' characters.
        """
        if self.text.startswith("#"):
            return self.text.count("#")
        return 0

    def display_markdown(self) -> str:
        label_text = f"{{#{self.label}}}" if self.label else ""
        return f"{self.text} {label_text}"

    def display_streamlit(self) -> None:
        st.markdown(f"{self.text}")


def display(
    *content: str | MultiDisplayer,
    mode: DisplayMode | None = None,
    output_path: Path | None = None,
) -> str:
    """
    Display content in the specified mode.

    Args:
        *content: Content to display (strings or MultiDisplayer objects)
        mode: Override the global display mode
        output_path: Path to write output to (for MARKDOWN and PYTHON modes)

    Returns:
        String representation of the content (for MARKDOWN and PYTHON modes)
    """
    result = []

    # Use provided mode or fall back to global config
    display_config = get_display_config()
    display_mode = mode if mode is not None else display_config.mode
    logger.info(f"Display mode: {display_mode}")
    # Use provided output path or fall back to global config
    out_path = output_path if output_path is not None else display_config.output_path

    for item in content:
        if isinstance(item, MultiDisplayer):
            if (
                display_mode == DisplayMode.MARKDOWN
                or display_mode == DisplayMode.PYTHON
            ):
                result.append(item.display_markdown())
            else:
                item.display_streamlit()
        else:
            item = str(item)
            if (
                display_mode == DisplayMode.MARKDOWN
                or display_mode == DisplayMode.PYTHON
            ):
                result.append(item)
            else:  # STREAMLIT
                st.markdown(item)
        result.append("\n")


    if display_mode == DisplayMode.MARKDOWN or display_mode == DisplayMode.PYTHON:
        output_string = "\n\n".join(result)
        if out_path is not None:
            # Write to the specified output path
            with open(out_path, "a") as f:
                f.write(output_string)

        return output_string
    return ""
