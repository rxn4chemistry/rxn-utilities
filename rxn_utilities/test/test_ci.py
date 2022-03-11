# LICENSED INTERNAL CODE. PROPERTY OF IBM.
# IBM Research Zurich Licensed Internal Code
# (C) Copyright IBM Corp. 2021
# ALL RIGHTS RESERVED

import yaml
from rxn_utilities.test.utils import FileFromContent
from rxn_utilities.ci import update_image_tag

VALUES_FILE_CONTENT = r"""
image:
  tag: old-tag

settings:
  a_field_containing_tag: a_tag_that_should_not_be_changed
"""

VALUES_FILE_WITH_COMPONENT_CONTENT = r"""
image:
  component_to_change:
    repository: cr.io/component_to_change_name
    tag: old-tag
  component_to_ignore:
    repository: cr.io/component_to_ignore_name
    tag: old-tag

settings:
  a_field_containing_tag: a_tag_that_should_not_be_changed
"""


def test_update_image_tag():
    new_tag = 'new_tag'
    with FileFromContent(VALUES_FILE_CONTENT) as test_file:
        update_image_tag(test_file.filename, new_tag)
        with open(test_file.filename, 'rt') as fp:
            values = yaml.full_load(fp)
        assert values['image']['tag'] == new_tag
        assert values['settings']['a_field_containing_tag'] == 'a_tag_that_should_not_be_changed'


def test_update_image_tag_in_component():
    new_tag = 'new_tag'
    with FileFromContent(VALUES_FILE_WITH_COMPONENT_CONTENT) as test_file:
        update_image_tag(test_file.filename, new_tag, image_name='component_to_change_name')
        with open(test_file.filename, 'rt') as fp:
            values = yaml.full_load(fp)
        assert 'tag' not in values['image']
        assert values['image']['component_to_change']['tag'] == new_tag
        assert values['image']['component_to_ignore']['tag'] == 'old-tag'
