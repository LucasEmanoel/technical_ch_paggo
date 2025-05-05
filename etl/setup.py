from setuptools import setup, find_packages

setup(
    name="etl_paggo",
    version="0.1",
    packages=find_packages(where="app"),
    package_dir={"": "app"},
)
