#!/usr/bin/env python

import setuptools

with open("D:\pygraphv\README.md", "r") as file:
    long_description = file.read()

if __name__ == '__main__':
    setuptools.setup(
        name="elth", 
        version="0.1", 
        author="farkon00",
        author_email="sammer2016sammer@gmail.com",
        description="Elth is python library, that makes generating elf binaries easy.",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/farkon00/elth",
        packages=setuptools.find_packages(),
        python_requires=">=3.6",
        license="MIT",
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
    )