#!/usr/bin/env python

from setuptools import find_packages, setup

if __name__ == "__main__":
    setup(
        packages=find_packages(),
        include_package_data = True,
        package_data={'': ['config/**']},
    )
