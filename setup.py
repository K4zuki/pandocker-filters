# Always prefer setuptools over distutils
from setuptools import setup, find_packages

requires = ["panflute>=1.10.3",
            "Pillow",
            "svgutils>=0.2.0",
            "svglib",
            "aafigure",
            "wavedrom",
            "pantable",
            ]

setup(
    name="pandoc_pandocker_filters",
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    description="Yet another set of pandoc filters",
    author="k4zuki",
    author_email="k.yamamoto.08136891@gmail.com",
    url="https://github.com/K4zuki/pandocker-filters",
    license="MIT",
    install_requires=requires,
    keywords=["pandoc", "markdown"],
    classifiers=["Development Status :: 4 - Beta",
                 "Programming Language :: Python :: 3.5",
                 "Programming Language :: Python :: 3.6",
                 ],
    python_requires=">=3.5,!=3.0.*,!=3.1.*,!=3.2.*",
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    entry_points={
        "console_scripts": [
            "pandocker-filters = pandoc_pandocker_filters:main",

            "pandocker-bitfield = pandoc_pandocker_filters.bitfield_inline:listed",
            "pandocker-bitfield-block = pandoc_pandocker_filters.BitField:main",
            "pandocker-bitfield-inline = pandoc_pandocker_filters.bitfield_inline:main",

            "pandocker-listingtable = pandoc_pandocker_filters.listingtable_inline:listed",
            "pandocker-listingtable-block = pandoc_pandocker_filters.ListingTable:main",
            "pandocker-listingtable-inline = pandoc_pandocker_filters.listingtable_inline:main",

            "pandocker-wavedrom-inline = pandoc_pandocker_filters.wavedrom_inline:main",

            "pandocker-rotateimage = pandoc_pandocker_filters.rotateimage_inline:listed",
            "pandocker-rotateimage-block = pandoc_pandocker_filters.RotateImage:main",
            "pandocker-rotateimage-inline = pandoc_pandocker_filters.rotateimage_inline:main",

            "pandocker-aafigure = pandoc_pandocker_filters.aafigure_inline:listed",
            "pandocker-aafigure-block = pandoc_pandocker_filters.AAFigure:main",
            "pandocker-aafigure-inline = pandoc_pandocker_filters.aafigure_inline:main",

            "pandocker-pantable-inline = pandoc_pandocker_filters.pantable_inline:main"
        ],
    },
)
