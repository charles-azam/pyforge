import typer
from pathlib import Path

app = typer.Typer(
    name="pyforge",
    no_args_is_help=True,
    pretty_exceptions_enable=False,
    context_settings={"help_option_names": ["-h", "--help"]},
)


@app.command(no_args_is_help=True)
def view(doc_path: Path):
    """
Interactive viewer with autoreload for a document that leverages the power of Streamlit.
    """
    pass


@app.command(no_args_is_help=True)
def markdown(doc_path: Path):
    """
Convert a document to plain pandoc markdown.
    """
    pass

@app.command(no_args_is_help=True)
def pdf(doc_path: Path):
    """
Convert a document to PDF using pandoc.
    """
    pass

if __name__ == "__main__":
    app()
 