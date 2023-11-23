import os

import pip
from setuptools import find_packages, setup

setup(
    name='Moby_Land',
    version='0.3.1',
    author='Adam Boesky',
    author_email='apboesky@gmail.com',
    description='A place for all of my gadgets.',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
    install_requires=['matplotlib', 'numpy'],
)

# To republish:
# 1. bump version nuber
# 2. python setup.py sdist
# 3. twine upload dist/*
