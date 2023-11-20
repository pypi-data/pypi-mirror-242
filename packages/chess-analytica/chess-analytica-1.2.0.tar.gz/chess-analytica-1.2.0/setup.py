from setuptools import setup

from codecs import open
from os import path

HERE = path.abspath(path.dirname(__file__))

setup(
    name="chess-analytica",
    version="1.2.0",
    description="Making chess analytics easy.",
    long_description=open('README.rst').read(),
    long_description_content_type='text/x-rst',
    url="https://github.com/AronFrish/Chess-Analytica",
    author="Aron Frishberg",
    author_email="frishberg@uchicago.edu",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "Topic :: Games/Entertainment :: Board Games",
        "Topic :: Games/Entertainment :: Turn Based Strategy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    project_urls={
        "Documentation": "https://chess-analytica.readthedocs.io",
    },
    packages=["chess_analytica"],
    include_package_data=True,
    install_requires=["chess", "urllib3"]
)