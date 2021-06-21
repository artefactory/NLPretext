# type: ignore[attr-defined]

import typer
from nlpretext import __version__
from nlpretext.cli import dialogs
from rich.console import Console

app = typer.Typer(
    name="nlpretext",
    help="All the goto functions you need to handle NLP use-cases, integrated in NLPretext",
    add_completion=True,
)
app.add_typer(dialogs.app, name="dialogs")
console = Console()


def version_callback(value: bool):
    """Prints the version of the package."""
    if value:
        console.print(f"[yellow]nlpretext[/] version: [bold blue]{__version__}[/]")
        raise typer.Exit()
