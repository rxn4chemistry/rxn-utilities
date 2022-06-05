import random

import click

from rxn.utilities.files import dump_list_to_file, load_list_from_file


@click.command()
@click.argument("input_file", type=str, required=True)
@click.argument("output_file", type=str, required=True)
@click.option("--seed", type=int, default=42, help="Random seed")
def main(input_file: str, output_file: str, seed: int):
    """Shuffle a file in a deterministic order (the same seed always reorders
    files of the same number of lines identically).

    Useful, as an example, to shuffle both source and target files identically.
    """
    random.seed(seed)

    lines = load_list_from_file(input_file)
    random.shuffle(lines)
    dump_list_to_file(lines, output_file)


if __name__ == "__main__":
    main()
