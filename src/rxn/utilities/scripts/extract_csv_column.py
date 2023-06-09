from pathlib import Path

import click

from ..files import dump_list_to_file, iterate_csv_column


@click.command(context_settings=dict(show_default=True))
@click.option(
    "--csv_file",
    "-i",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    required=True,
    help="CSV file.",
)
@click.option(
    "--column",
    "-c",
    type=str,
    required=True,
    help="Column to extract.",
)
@click.option(
    "--output_txt",
    "-o",
    type=click.Path(writable=True, path_type=Path),
    required=True,
    help="Where to save the extracted values (as a file with one value per line).",
)
@click.option(
    "--delimiter",
    "-d",
    type=str,
    default=",",
    help="CSV delimiter.",
)
def main(csv_file: Path, column: str, output_txt: Path, delimiter: str) -> None:
    """
    Extract a column of a CSV file into its own file (one value per line).
    """
    dump_list_to_file(iterate_csv_column(csv_file, column, delimiter), output_txt)


if __name__ == "__main__":
    main()
