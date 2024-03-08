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

from q2_types.feature_data import FeatureData
from q2_types.feature_data import Sequence
from q2_types.feature_table import FeatureTable
from q2_types.feature_table import Frequency
from q2_types.per_sample_sequences import PairedEndSequencesWithQuality
from q2_types.sample_data import SampleData
from qiime2.plugin import Bool
from qiime2.plugin import Citations
from qiime2.plugin import Float
from qiime2.plugin import Int
from qiime2.plugin import Plugin
from qiime2.plugin import Range
from qiime2.plugin import Str
from qiime2.plugin import Threads

import q2_thapbi_pict

citations = Citations.load("citations.bib", package="q2_thapbi_pict")
plugin = Plugin(
    name="q2-thapbi-pict",
    version=q2_thapbi_pict.__version__,
    website="https://github.com/peterjc/q2-thapbi-pict",
    package="q2_thapbi_pict",
    citations=[citations["Cock2023"]],
    description=(
        "This QIIME 2 plugin provides support for running "
        "some of the THAPBI PICT functionality."
    ),
    short_description="Qiime2 plugin for THAPBI PICT.",
)


plugin.methods.register_function(
    function=q2_thapbi_pict.prepare_reads_sample_tally,
    inputs={"demultiplexed_seqs": SampleData[PairedEndSequencesWithQuality]},
    parameters={
        "primer_definition": Str,
        "abundance": Int % Range(2, None),
        "abundance_fraction": Float
        % Range(0, 1, inclusive_start=True, inclusive_end=True),
        "flip": Bool,
        "cpu": Threads,
        "debug": Bool,
    },
    outputs=[
        ("asv_vs_sample_table", FeatureTable[Frequency]),
        ("asv_sequences", FeatureData[Sequence]),
    ],
    input_descriptions={
        "demultiplexed_seqs": "The paired-end sequences to be merged and tallied."
    },
    parameter_descriptions={
        "primer_definition": (
            "Semi-colon separated list of amplicon and primer definitions in the "
            "form <NAME>:<LEFT>:<RIGHT>:<MINLEN>:<MAXLEN> where IUPAC ambiguitity "
            "codes can be used for the primer sequences, and the lengths can be "
            "omitted defaulting to 100 and 1000bp."
        ),
        "abundance": (
            "Minimum abundance applied to unique marker sequences in each sample "
            "(i.e. each FASTQ pair). Default 100."
            # "May be increased based on "
            # "negative controls. Half this value is applied to synthetic controls."
        ),
        "abundance_fraction": (
            "Minimum abundance fraction, low frequency noise threshold applied to "
            "unique marker sequences in each sample. Default 0.001 meaning 0.1%. "
            # "May be increased based on synthetic controls. Half this value is "
            # "applied to negative controls."
        ),
        "flip": "Also check reverse complement strand for primers.",
        "cpu": "How many threads to use, zero meaning all available.",
        "debug": "Run in debug mode, use with --verbose enabled.",
    },
    output_descriptions={
        "asv_vs_sample_table": "Feature table, counts of ASV sequences vs samples.",
        "asv_sequences": "Accepted ASV sequences matching the feature table.",
    },
    name="Prepare reads and tally by sample using THAPBI PICT",
    description=(
        "Takes paired (raw) FASTQ files demultiplexed per sample. "
        "Runs THAPBI PICT prepare-reads (which calls Flash to merge "
        "them, deuplicates, then calls CutAdapt to find, remove and "
        "separate the amplicon(s) by their primer sequences), then "
        "THAPBI PICT sample-tally which optionally uses UNOISE for "
        "read-correction/denoising, then applies abundance thresholds, "
        "and outputs a BIOM table of counts of accepted Amplicon "
        "Sequence Variants (ASVs, or unique seqs) per sample."
    ),
    citations=[
        citations["Cock2023"],
        citations["Magoc2011"],
        citations["Martin2011"],
        citations["Edgar2016"],
        citations["Rognes2016"],
    ],
)
