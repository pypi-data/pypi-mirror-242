from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.9'
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
    keywords=[],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
	"Operating System :: Unix",
    ],
    python_requires=">=3.6",
)
