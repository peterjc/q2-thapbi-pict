# Copyright 2024 by Peter Cock, The James Hutton Institute.
# All rights reserved.
# This file is part of the THAPBI Phytophthora ITS1 Classifier Tool (PICT),
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
"""setuptools based setup script for the Qiime2 plugin for THAPBI PICT.

This uses setuptools which is now the standard python mechanism for installing
packages (and is used internally by the tool pip). If you have downloaded and
uncompressed the THAPBI PICT source code, or fetched it from git, for the
simplest installation try one of these commands::

    pip install .

Or::

    python setup.py install

Typically however, since we have released this software via cond, you don't
need to download it first. Instead just run::

    conda install q2-thapbi-pict

Once installed, you should be able to use the plugin via the ``qiime2``
command (the Qiime2 command line interface, q2cli).
"""

from __future__ import print_function  # noqa: UP010
from __future__ import with_statement  # noqa: UP010

import sys

try:
    # from setuptools import find_packages
    from setuptools import setup
except ImportError:
    sys.exit(
        "We need the Python library setuptools to be installed. "
        "Try running: python -m ensurepip"
    )


# Make sure we have the right Python version.
if sys.version_info[:2] < (3, 7):  # noqa: UP036
    sys.exit(
        "THAPBI PICT requires Python 3.7 or later. "
        "Python %d.%d detected.\n" % sys.version_info[:2]
    )

# We define the version number in thapbi_pict/__init__.py
# Here we can't use "import thapbi_pict" then "thapbi_pict.__version__"
# as that would tell us the version already installed (if any).
__version__ = "Undefined"
with open("q2_thapbi_pict/__init__.py") as handle:
    for line in handle:
        if line.startswith("__version__ = "):
            exec(line.strip())
            break

# Load our rsStructuredText file README.rst as the long description.
#
# Without declaring an encoding, decoding a problematic character in the file
# may fail on Python 3 depending on the user's locale. By explicitly checking
# it is ASCII (could use latin1 or UTF8 if needed later), if any invalid
# character does appear in our README, this will fail for everyone.
with open("README.rst", "rb") as handle:
    readme_rst = handle.read().decode("ascii")

setup(
    name="q2_thapbi_pict",
    version=__version__,
    author="Peter Cock",
    author_email="peter.cock@hutton.ac.uk",
    url="https://github.com/peterjc/q2-thapbi-pict",  # For now at least
    download_url="https://github.com/peterjc/q2-thapbi-pict",
    description="Qiime2 plugin for THAPBI PICT.",
    project_urls={
        "Documentation": "https://thapbi-pict.readthedocs.io/",  # Main package
        "Source": "https://github.com/peterjc/q2-thapbi-pict/",
        "Tracker": "https://github.com/peterjc/q2-thapbi-pict/issues",
    },
    long_description=readme_rst,
    long_description_content_type="text/x-rst",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: Freely Distributable",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    python_requires=">=3.7",
    entry_points={
        "qiime2.plugins": ["q2-thapbi-pict=q2_thapbi_pict.plugin_setup:plugin"]
    },
    packages=["q2_thapbi_pict"],
    package_data={
        "q2_thapbi_pict": ["citations.bib"],
    },
    include_package_data=True,
    install_requires=[
        # Tested on thapbi_pict 1.0.12 under Python 3.8 from
        # conda installed qiime2 version 2024.2 or 2023.5
        "thapbi_pict >=1.0.12,<1.1",  # Upper bound a precaution
        # Qiime packages not on PyPI but via qiime2 conda channel...
        # Need at least 2023.5 for Collections data type
        "q2-types >=2023.5",
        "q2cli >=2023.5",
        "biom-format >=2.1.12",
    ],
)
