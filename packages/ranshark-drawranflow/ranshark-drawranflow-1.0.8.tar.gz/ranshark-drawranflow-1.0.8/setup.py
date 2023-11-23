from setuptools import setup,find_packages
from distutils.core import setup
from pathlib import Path
import os

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'README.md')) as f:
    long_description = f.read()

setup(
    long_description=long_description,
    long_description_content_type='text/markdown',
        install_requires=[
        'Django~=4.2.7',
        'celery~=5.3.4',
        'pandas~=1.3.3',
        'pyshark~=0.6',

    ],
)
