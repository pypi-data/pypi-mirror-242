from __future__ import print_function
from setuptools import setup, find_packages
import sys

setup(
    name="mjm",
    version="0.2.1" ,
    author="maijiaming",
    description="hello world",
    # long_description=open("README.rst",encoding="utf8").read(),
    packages=find_packages(),
    package_data={
    #"gsjtu.postgresql":["plpython/*"],

    },
    install_requires=[
        "pandas"
        ],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7"
    ],
)

#python  setup.py sdist &  twine upload dist/* & rd /s /q dist & rd /s /q lmf.egg-info & python -m pip install lmf==2.3.0