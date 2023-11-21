from setuptools import setup, find_packages
import os
import sys

setup(
    name="wmagentscripts",
    author="Hasan Ozturk",
    version="0.0.2",
    description="WMAgentScripts",
    python_requires=">=3.6",
    package_dir={"": "src/python"},
    packages=find_packages(include="src/python"),
    install_requires=["pymongo", "sqlalchemy"],
)
