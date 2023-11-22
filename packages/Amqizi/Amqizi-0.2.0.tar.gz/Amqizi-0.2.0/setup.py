from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.2.0'
DESCRIPTION = 'A Basic Hello World package'

# Setting up
setup(
    name="Amqizi",
    version=VERSION,
    author="MrRobinnn",
    author_email="spree.wolf@protonmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['hello','hey','bye'],
    url = "https://github.com/MrRobinnn/simple-pkg",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
	"Operating System :: OS Independent"
    ],
    python_requires=">=3.6",
)
