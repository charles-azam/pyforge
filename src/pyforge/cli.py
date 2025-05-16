import typer

app = typer.Typer(
    name="pyforge",
    no_args_is_help=True,
    pretty_exceptions_enable=False,
    context_settings={"help_option_names": ["-h", "--help"]},
)

@app.command(no_args_is_help=True)
def hello(name: str, formal: bool = False):
    """
    Dit bonjour à NAME.

    Si --formal est utilisé, dit bonjour formellement.
    """
    if formal:
        print(f"Bonjour Monsieur/Madame {name}")
    else:
        print(f"Bonjour {name}")

@app.command(no_args_is_help=True)
def goodbye(name: str, farewell: str = "Au revoir"):
    """
    Dit au revoir à NAME avec un message optionnel.
    """
    print(f"{farewell} {name}")

if __name__ == "__main__":
    app()