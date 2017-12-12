# Always prefer setuptools over distutils
from setuptools import find_packages
# To use a consistent encoding
from codecs import open
from os import path
from distutils.core import setup

requires = ["panflute"]

setup(
    name="pandoc_pandocker_filters",
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    version="0.0.4",  # Ideally should be same as your GitHub release tag varsion
    description="Yet another set of pandoc filters",
    author="k4zuki",
    author_email="k.yamamoto.08136891@gmail.com",
    url="https://github.com/K4zuki/pandocker-filters",
    install_requires=requires,
    keywords=["pandoc", "markdown"],
    classifiers=[],
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        "console_scripts": [
            "pandocker-bitfield = pandoc_pandocker_filters.BitField:main",
            "pandocker-bitfield-inline = pandoc_pandocker_filters.bitfield_inline:main",
            "pandocker-listingtable = pandoc_pandocker_filters.ListingTable:main",
            "pandocker-listingtable-inline = pandoc_pandocker_filters.listingtable_inline:main",
            "pandocker-wavedrom-inline = pandoc_pandocker_filters.wavedrom_inline:main",
            "pandocker-rotateimage = pandoc_pandocker_filters.RotateImage:main",
            "pandocker-rotateimage-inline = pandoc_pandocker_filters.rotateimage_inline:main",
        ],
    },
)
