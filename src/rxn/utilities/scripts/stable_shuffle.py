from pathlib import Path

import click

from rxn.utilities.files import stable_shuffle


@click.command()
@click.argument(
    "input_file", type=click.Path(exists=True, path_type=Path), required=True
)
@click.argument(
    "output_file", type=click.Path(writable=True, path_type=Path), required=True
)
@click.option(
    "--csv",
    is_flag=True,
    default=False,
    help=(
        "Indicates that the file is a CSV, i.e. the first line"
        " should not be included in the shuffling."
    ),
)
@click.option("--seed", type=int, default=42, help="Random seed")
def main(input_file: Path, output_file: Path, csv: bool, seed: int) -> None:
    """Shuffle a file in a deterministic order (the same seed always reorders
    files of the same number of lines identically).

    Useful, as an example, to shuffle both source and target files identically.
    """
    stable_shuffle(
        input_file=input_file, output_file=output_file, seed=seed, is_csv=csv
    )


if __name__ == "__main__":
    main()
