import io
import re

from setuptools import setup

__version__ = re.search(
    r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
    io.open('rxn_utilities/__init__.py', encoding='utf_8_sig').read()
).group(1)

setup(
    name='rxn_utilities',
    version=__version__,
    author='IBM RXN team',
    packages=[
        'rxn_utilities'
    ],
    package_data={
        'rxn_utilities': ['py.typed']
    },
    install_requires=[
        'attrs>=19.1.0',
        'requests>=2.23.0'
    ]
)
