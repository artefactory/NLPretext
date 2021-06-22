from typing import List

import typer
from nlpretext.preprocessor import Preprocessor
from nlpretext.textloader import TextLoader
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def run(
    input: List[str] = typer.Option(
        [],
        "-i",
        "--input",
        case_sensitive=False,
        help="List of files that will be preprocessed",
    ),
    output: str = typer.Option(
        None,
        "-o",
        "--output",
        case_sensitive=False,
        help="File that will store the result of the preprocessing",
    ),
) -> None:
    """Prints a greeting for a giving name.

    Args:

        input: List of files that will be preprocessed

        output: File that will store the result of the preprocessing
    """
    text_loader = TextLoader()
    preprocessor = Preprocessor()
    preprocessed_text_dataframe = text_loader.read_text(input, preprocessor=preprocessor)
    preprocessed_text_dataframe.to_parquet(output)
