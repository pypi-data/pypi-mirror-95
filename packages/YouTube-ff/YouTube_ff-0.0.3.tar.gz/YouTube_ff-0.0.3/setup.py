from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.3'
DESCRIPTION = 'A module to search and download youtube videos.'


# Setting up
setup(
    name="YouTube_ff",
    version=VERSION,
    author="Python.Stuff",
    author_email="<srinathngudi11@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['pytube'],
    keywords=['python', 'youtube', 'youtube_ff'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
