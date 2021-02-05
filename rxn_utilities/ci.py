# LICENSED INTERNAL CODE. PROPERTY OF IBM.
# IBM Research Zurich Licensed Internal Code
# (C) Copyright IBM Corp. 2021
# ALL RIGHTS RESERVED

"""Utilities for RXN CI."""
import yaml


def update_image_tag(values_yaml_filepath: str, image_tag: str) -> None:
    """
    Update image tag in the given value file.

    Args:
        values_yaml_filepath (str): path to a .yaml values file.
        image_tag (str): image tag used for the update.
    """
    with open(values_yaml_filepath, 'rt') as fp:
        values = yaml.full_load(fp)
    values['image']['tag'] = image_tag
    with open(values_yaml_filepath, 'wt') as fp:
        yaml.dump(values, fp)
