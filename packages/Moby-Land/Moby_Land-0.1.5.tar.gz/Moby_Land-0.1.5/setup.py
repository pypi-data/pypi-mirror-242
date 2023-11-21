from setuptools import setup, find_packages

def read_requirements():
    with open('requirements.txt') as req:
        return req.read().strip().split('\n')

setup(
    name='Moby_Land',
    version='0.1.5',
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
    install_requires=read_requirements(),  # Use the read_requirements function
)

# To republish:
# 1. bump version nuber
# 2. python setup.py sdist
# 3. twine upload dist/*
