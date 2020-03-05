import io
import re

from setuptools import setup
__version__ = re.search(
    r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
    io.open('__init__.py', encoding='utf_8_sig').read()
).group(1)

setup(
    name='rxn_utilities',
    version=__version__,
    author='IBM RXN team',
    packages=[
        'rxn_utilities'
    ]
)
