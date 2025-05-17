from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from pyforge.note import (Citation, DisplayMode, DocumentConfig, Figure,
                          Reference, Table, Title, display,
                          set_markdown_display_mode,
                          unset_markdown_display_mode)


def test_document_config_markdown():
    config = DocumentConfig(
        title="Test Document", author="Test Author", date="2025-05-17"
    )
    markdown = config.display_markdown()
    assert "Test Document" in markdown
    assert "Test Author" in markdown
    assert "2025-05-17" in markdown


def test_figure_markdown():
    fig = Figure(Path("test/path.png"), "Test Caption", "fig:test")
    markdown = fig.display_markdown()
    assert "![Test Caption](test/path.png)" in markdown
    assert "{#fig:test}" in markdown


def test_table_markdown():
    data = pd.DataFrame({"A": [1, 2, 3], "B": ["x", "y", "z"]})
    table = Table(data, "Test Table", "tbl:test")
    markdown = table.display_markdown()
    assert "Test Table" in markdown
    assert "{#tbl:test}" in markdown
    assert "|" in markdown  # Table formatting


def test_title_markdown():
    title = Title("Test Title", "sec:test")
    markdown = title.display_markdown()
    assert "Test Title" in markdown
    assert "{#sec:test}" in markdown


@patch("pyforge.note.get_display_config")
def test_display_markdown_mode(mock_get_config):
    mock_config = MagicMock()
    mock_config.mode = DisplayMode.MARKDOWN
    mock_get_config.return_value = mock_config

    title = Title("Test Title")
    result = display(title, mode=DisplayMode.MARKDOWN)
    assert "Test Title" in result
