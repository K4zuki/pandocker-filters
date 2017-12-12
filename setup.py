# Always prefer setuptools over distutils
from setuptools import find_packages
# To use a consistent encoding
from codecs import open
from os import path
from distutils.core import setup

requires = ["panflute"]

setup(
    name="pandoc_pandocker_filters",
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    version="0.0.2",  # Ideally should be same as your GitHub release tag varsion
    description="Yet another pandoc filter group",
    author="k4zuki",
    author_email="k.yamamoto.08136891@gmail.com",
    url="https://github.com/K4zuki/pandocker-filters",
    install_requires=requires,
    keywords=["pandoc", "markdown"],
    classifiers=[],
)
