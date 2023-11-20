from setuptools import setup, find_packages

from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="apsystems-ez1",
    version="0.1.7",
    description="The APsystems EZ1 Python library can be used to interact with APsystems EZ1 Microinverters local API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://apsystems-ez1.readthedocs.io/",
    author="Leo Tiedt, Sonnenladen GmbH",
    author_email="l.tiedt@sonnenladen.de",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ],
    packages=["APsystems_EZ1"],
    include_package_data=True,
    install_requires=["requests~=2.31.0"]
)