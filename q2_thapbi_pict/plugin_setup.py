# Copyright 2024 by Peter Cock, The James Hutton Institute.
# All rights reserved.
# This file is part of the THAPBI Phytophthora ITS1 Classifier Tool (PICT),
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
"""Registering the plugin within the Qiime2 ecosystem."""

# from qiime2.plugin import (Plugin, List, Str, Float, Bool, Int, Citations,
#                           Range, Choices)
# from q2_types.feature_table import FeatureTable, RelativeFrequency, Frequency
# from q2_types.feature_data import FeatureData, Taxonomy, Sequence
# from q2_feature_classifier._taxonomic_classifier import TaxonomicClassifier

from qiime2.plugin import Plugin
from qiime2.plugin import Citations

from . import __version__

citations = Citations.load("citations.bib", package="q2_thapbi_pict")
plugin = Plugin(
    name="q2-thapbi-pict",
    version=__version__,
    website="https://github.com/peterjc/q2-thapbi-pict",
    package="q2_thapbi_pict",
    citations=[citations["Cock2023"]],
    description=(
        "This QIIME 2 plugin provides support for running "
        "some of the THAPBI PICT functionality."
    ),
    short_description="Qiime2 plugin for THAPBI PICT.",
)
