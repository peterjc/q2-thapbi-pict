# Copyright 2024 by Peter Cock, The James Hutton Institute.
# All rights reserved.
# This file is part of the THAPBI Phytophthora ITS1 Classifier Tool (PICT),
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
"""Qiime2 plugin for THAPBI PICT's prepare-reads and sample-tally."""

import os
import sys
import tempfile

import biom
from q2_types.feature_data import DNAIterator
from q2_types.per_sample_sequences import SingleLanePerSamplePairedEndFastqDirFmt


def setup_rawdata(qza_folder: str, raw_data: str, debug: bool = False) -> None:
    """Prepare FASTQ symlinks to paired reads defined in the MANIFEST."""
    # Must look at the MANIFEST to infer sample pairing, since in the examples
    # I am looking at they are named <SAMPLE>_<N>_L001_R<FR>_001.fastq.gz
    # where <SAMPLE> is the prefix, <FR> is 1 or 2 as in ..._R1_... or ..._R2__...
    # but <N> runs from 1 to 2*N where there are N pairs and 2*N files!
    #
    # i.e. Cannot assume <PREFIX>_R1_001.fastq.gz with <PREFIX>_R2_001.fastq.gz
    assert isinstance(qza_folder, str)
    assert isinstance(raw_data, str)
    fwd = {}
    rev = {}
    if debug:
        sys.stderr.write(f"DEBUG: Parsing MANIFEST in {qza_folder}\n")
    with open(os.path.join(qza_folder, "MANIFEST")) as handle:
        line = handle.readline()
        if line != "sample-id,filename,direction\n":
            raise ValueError(f"Unexpected MANIFEST header: {line}")
        for line in handle:
            sample, filename, direction = line.rstrip("\n").split(",")
            if direction == "forward":
                fwd[sample] = filename
            elif direction == "reverse":
                rev[sample] = filename
            else:
                raise ValueError(f"Unexpected direction in MANIFEST line: {line}")
            if not filename.endswith(".fastq.gz"):
                raise ValueError(
                    f"Unexpected extension for {sample} {direction}: {filename}"
                )
    if len(fwd) != len(rev):
        raise ValueError(
            f"Mismatched {len(fwd)} forward vs {len(rev)} reverse samples in MANIFEST"
        )
    elif set(fwd) != set(rev):
        raise ValueError("Mismatched forward and reverse sample names in MANIFEST")
    if debug:
        sys.stderr.write(
            f"DEBUG: Making symlinks to {2*len(fwd)} FASTQ under {raw_data}\n"
        )
    for sample in fwd:
        os.symlink(
            os.path.join(qza_folder, fwd[sample]),
            os.path.join(raw_data, sample + "_R1.fastq.gz"),
        )
        os.symlink(
            os.path.join(qza_folder, rev[sample]),
            os.path.join(raw_data, sample + "_R2.fastq.gz"),
        )


def prepare_reads_sample_tally(
    demultiplexed_seqs: SingleLanePerSamplePairedEndFastqDirFmt,
    primer_definition: str,
    abundance: int = 100,
    abundance_fraction: float = 0.001,
    flip: bool = False,
    cpu: int = 0,
    debug: bool = False,
) -> (biom.Table, DNAIterator):
    """THAPBI PICT's prepare-reads and sample-tally.

    Starts by making a temporary workind directory. Into this it creates a
    ``raw_data/`` folder of symlinks using ``<SAMPLE>_R1.fastq.gz`` and
    ``<SAMPLE>_R2.fastq.gz`` naming based on the QZA file manifest. Then takes
    the given primer definitations, and sets up a dummy THAPBI PICT database
    using those but no reference sequences.

    The other parameters are passed to THAPBI PICT ``prepare-reads`` and
    ``sample-tally`` as they are.
    """
    tmp_obj = tempfile.TemporaryDirectory()
    tmp_dir = tmp_obj.name

    # Setup the FASTQ inputs (could extend to multiple QZA files...)
    raw_data = os.path.join(tmp_dir, "raw_data")
    os.mkdir(raw_data)
    setup_rawdata(str(demultiplexed_seqs), raw_data, debug=debug)

    # Setup the dumming THAPBI PICT database
    # ...

    # Call THAPBI PICT prepare-reads
    # ...

    # Call THAPBI PICT sample-tally
    # ...

    # Wrap output for QIIME2
    # ...

    if debug:
        sys.stderr.write(f"DEBUG: Please delete {tmp_dir}\n")
    else:
        tmp_obj.cleanup()
    return None, None
