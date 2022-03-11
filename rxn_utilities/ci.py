# LICENSED INTERNAL CODE. PROPERTY OF IBM.
# IBM Research Zurich Licensed Internal Code
# (C) Copyright IBM Corp. 2021
# ALL RIGHTS RESERVED
"""Utilities for RXN CI."""
import yaml
import logging
from typing import Optional

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def update_image_tag(
    values_yaml_filepath: str, image_tag: str, image_name: Optional[str] = None
) -> None:
    """
    Update image tag in the given value file.

    Args:
        values_yaml_filepath (str): path to a .yaml values file.
        image_tag (str): image tag used for the update.
        image_name (str, default): optional image name. Defaults to None, a.k.a.,
            do not target the image name for tag update.
    """
    with open(values_yaml_filepath, 'rt') as fp:
        values = yaml.full_load(fp)
    # NOTE: handling chart values nesting components inside the 'image' key.
    # standard values.yaml:
    # ```yaml
    # image:
    #   tag: an-image-tag
    #   repository: cr.io/namespace/image-name
    # ```
    # component-based values.yaml:
    # ```yaml
    # image:
    #   component_a:
    #       tag: an-image-tag
    #       repository: cr.io/namespace/image-name-component-a
    #   component_b:
    #       tag: another-image-tag
    #       repository: cr.io/namespace/image-name-component-b
    # ```
    if 'tag' not in values['image']:
        if image_name is not None:
            for component, component_values in values['image'].items():
                if 'tag' in component_values and component_values.get('repository',
                                                                      '').endswith(image_name):
                    component_values['tag'] = image_tag
                else:
                    logger.warning(
                        f'component={component} does not contain tag field or {image_name} not present in {component_values}'
                    )
        else:
            logger.warning('tag field not present and image_name not provided, skipping...')
    else:
        values['image']['tag'] = image_tag
    with open(values_yaml_filepath, 'wt') as fp:
        yaml.dump(values, fp)
