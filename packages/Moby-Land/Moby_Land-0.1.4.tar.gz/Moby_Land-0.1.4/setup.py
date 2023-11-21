from setuptools import setup, find_packages

setup(
    name='Moby_Land',
    version='0.1.4',
    author='Adam Boesky',
    author_email='apboesky@gmail.com',
    description='A place for all of Adam\' gadgets.',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.0',
)

# To republish:
# 1. bump version nuber
# 2. python setup.py sdist
# 3. twine upload dist/*
