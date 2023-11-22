from setuptools import setup, find_packages
import os

VERSION = '1.0.0'
DESCRIPTION = 'Simple script containing some ANSI escape codes.'

# Setting up
setup(
    name="ender_ansi",
    version=VERSION,
    author="Endercat126",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'colour', 'ansi'],
    classifiers=[
        "Programming Language :: Python :: 3"
    ]
)