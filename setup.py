# LICENSED INTERNAL CODE. PROPERTY OF IBM.
# IBM Research Zurich Licensed Internal Code
# (C) Copyright IBM Corp. 2021
# ALL RIGHTS RESERVED

import io
import re

from setuptools import setup

match = re.search(
    r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
    io.open('rxn_utilities/__init__.py', encoding='utf_8_sig').read()
)
if match is None:
    raise SystemExit('Error when getting the version from rxn_utilities/__init__.py')
__version__ = match.group(1)

setup(
    name='rxn_utilities',
    version=__version__,
    author='IBM RXN team',
    scripts=['bin/update-image-tag'],
    packages=['rxn_utilities'],
    package_data={'rxn_utilities': ['py.typed']},
    install_requires=['attrs>=21.2.0', 'requests>=2.23.0', 'pyyaml>=5.3.1', 'minio>=6.0.0'],
    extras_require={
        'dev':
            [
                'flake8>=3.7.9',
                'mark>=0.2',
                'mypy>=0.910',
                'pytest>=5.3.4',
                'pytest-cov>=2.8.1',
                'types-pyYAML>=5.4.3',
                'types-requests>=0.1.12',
                'yapf>=0.31.0',
            ],
    },
)
