"""Setup/build/install script for optrix."""

import os

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))


with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

with open(os.path.join(here, "requirements.txt"), encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="optrix",
    version="0.0.1a1",
    description=("A package for calculating ray propagation using matrix methods."),
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/joaopedrobiu6/optrix",
    author="João Pedro Ferreira Biu",
    author_email="joaopedrofbiu@tecnico.ulisboa.pt",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    keywords="optics, matrix, ray, propagation, paraxial, raytracing",
    packages=find_packages(exclude=["docs", "tests", "examples"]),
    include_package_data=True,
    install_requires=requirements,
    python_requires=">=3.8",
    project_urls={
        "Issues Tracker": "https://github.com/joaopedrobiu6/optrix/issues",
        "Source Code": "https://github.com/joaopedrobiu6/optrix/",
    },
)