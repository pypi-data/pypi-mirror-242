from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'A simple python package to get the weather of any city'

setup(
    name="personal-tracker",
    version=VERSION,
    author="Nhuengzii (Anawat Moonmanee)",
    author_email="<32nhueng@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=["ultralytics", "opencv-python","opencv-contrib-python"],
)
