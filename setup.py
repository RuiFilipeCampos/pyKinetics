# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 15:06:37 2020

@author: Rui Campos
"""

import setuptools

with open("README.md.txt", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyKinetics", # Replace with your own username
    version="0.0.3",
    author="Rui Filipe de Sousa Campos",
    author_email="ruifilipedesousacampos@gmail.com",
    description="A simple package that allows you to construct and simulate any biokinetical model.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RuiFilipeCampos/pyKinetics",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)