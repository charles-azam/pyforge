import importlib.util
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from pdb import run

import typer

from pyforge.common import get_logger
from pyforge.note import (DisplayMode, run_file_with_streamlit,
                          set_markdown_display_mode,
                          unset_markdown_display_mode)

app = typer.Typer(
    name="pyforge",
    no_args_is_help=True,
    pretty_exceptions_enable=False,
    context_settings={"help_option_names": ["-h", "--help"]},
)

logger = get_logger(__name__)


@app.command(no_args_is_help=True)
def markdown(doc_path: Path, output_path: Path = None):
    """
    Convert a document to plain pandoc markdown.

    Args:
        doc_path: Path to the Python document
        output_path: Path to write the markdown output (defaults to same name with .md extension)
    """
    if output_path is None:
        output_path = doc_path.with_suffix(".md")
        output_path.write_text("")

    logger.info(f"Converting {doc_path} to markdown at {output_path}")

    set_markdown_display_mode(output_path=output_path)
    try:
        module_name = doc_path.stem
        spec = importlib.util.spec_from_file_location(module_name, doc_path)
        assert spec is not None
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
    finally:
        unset_markdown_display_mode()


@app.command(no_args_is_help=True)
def view(doc_path: Path, output_path: Path = None):
    """
    View a document with streamlit.

    Args:
        doc_path: Path to the Python document
        output_path: Path to write the markdown output (defaults to same name with .md extension)
    """
    arguments = ["--browser.gatherUsageStats", "false", "--server.runOnSave", "true"]
    logger.info(f"Viewing {doc_path} with streamlit at {output_path}")
    run_file_with_streamlit(
        filepath=doc_path,
        arguments=arguments,
    )
