from setuptools import setup, find_packages
import os
import sys

setup(
    name="wmagentscripts",
    author="Hasan Ozturk",
    version="0.0.3",
    description="WMAgentScripts",
    python_requires=">=3.6",
        packages=find_packages(where='src'),
    package_dir={'': 'src'},
    #package_dir={"": ".", 'wmagentscripts':'./src/python'},
    #packages=["wmagentscripts"],
    #packages=['src/python/Cache', 'src/python/Databases'],
    install_requires=["pymongo", "sqlalchemy"],
)
