# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname('/Users/dibia/OneDrive/Documents/Projects/Finished/pyez_stats/'))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="pyez_stats",
    version="0.1.1",
    description="stats library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pyez_stats.readthedocs.io/",
    author="Jason DiBiase",
    author_email="dibiasej3@gmail.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent"
    ],
    packages=["pyez_stats"],
    include_package_data=True,
    install_requires=["numpy", "scipy", "matplotlib"]
)