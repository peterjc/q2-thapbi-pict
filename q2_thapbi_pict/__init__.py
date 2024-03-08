# Copyright 2024 by Peter Cock, The James Hutton Institute.
# All rights reserved.
# This file is part of the THAPBI Phytophthora ITS1 Classifier Tool (PICT),
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
"""Qiime2 plugin for THAPBI PICT."""

# Qiime2 plugin convention is one file named per function
# with the same name but a leading underscore (as private).
# These are publicly exported from the main plugin namespace
# via __all__:
from ._prepare_reads_sample_tally import prepare_reads_sample_tally

__version__ = "0.0.1"


__all__ = ["prepare_reads_sample_tally"]
