# Copyright 2024 by Peter Cock, The James Hutton Institute.
# All rights reserved.
# This file is part of the THAPBI Phytophthora ITS1 Classifier Tool (PICT),
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
"""Qiime2 plugin for THAPBI PICT's prepare-reads and sample-tally."""

import sys

import biom
from q2_types.feature_data import DNAIterator
from q2_types.per_sample_sequences import SingleLanePerSampleSingleEndFastqDirFmt


def prepare_reads_sample_tally(
    demultiplexed_seqs: SingleLanePerSampleSingleEndFastqDirFmt,
    abundance: int = 100,
    abundance_fraction: float = 0.001,
    flip: bool = False,
    cpu: int = 0,
) -> (biom.Table, DNAIterator):
    """THAPBI PICT's prepare-reads and sample-tally."""
    sys.stderr.write(f"DEBUG: Calling THAPBI PICT with {str(demultiplexed_seqs)}\n")
