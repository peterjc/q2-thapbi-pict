# Copyright 2024 by Peter Cock, The James Hutton Institute.
# All rights reserved.
# This file is part of the THAPBI Phytophthora ITS1 Classifier Tool (PICT),
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
"""Qiime2 plugin for THAPBI PICT's prepare-reads and sample-tally."""

import os
import sys
import tempfile
from typing import Optional

from q2_types.feature_data import DNAFASTAFormat
from q2_types.feature_table import BIOMV210Format
from q2_types.per_sample_sequences import SingleLanePerSamplePairedEndFastqDirFmt
from thapbi_pict.__main__ import check_cpu
from thapbi_pict.__main__ import connect_to_db
from thapbi_pict.db_import import import_fasta_file
from thapbi_pict.prepare import main as prepare_reads
from thapbi_pict.sample_tally import main as sample_tally


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


def setup_marker(db_url: str, primer_definition: list, debug: bool = False) -> list:
    """Define primers in temporary THAPBI PICT database."""
    markers = []
    for primer in primer_definition:
        marker, left, right, minlen, maxlen = primer.split(":")
        minlen = int(minlen) if minlen else None
        maxlen = int(maxlen) if maxlen else None

        assert db_url.startswith("sqlite:///") and db_url.endswith(".sqlite")
        tmp_fasta = f"{db_url[10:-7]}.{marker}.fasta"
        with open(tmp_fasta, "w") as handle:
            handle.write(f"#{marker}\n")

        import_fasta_file(
            fasta_file=tmp_fasta,
            db_url=db_url,
            fasta_entry_fn=None,
            entry_taxonomy_fn=None,
            marker=marker,
            left_primer=left,
            right_primer=right,
            min_length=minlen,
            max_length=maxlen,
            name="Defining {marker}",
            debug=debug,
            validate_species=False,
            genus_only=False,
            tmp_dir=None,
        )
        markers.append(marker)
        if debug:
            sys.stderr.write(f"DEBUG: Created {marker} definition\n")
    return markers


# Can't say (dict[BIOMV210Format], dict[DNAFASTAFormat]) in Python 3.8
# and Qiime2 wants us to to say (BIOMV210Format, DNAFASTAFormat) instead.
# Likewise for the dict[demultiplexed_seqs] and list[str] for primers.
def prepare_reads_sample_tally(
    demultiplexed_seqs: SingleLanePerSamplePairedEndFastqDirFmt,
    primer_definition: str,
    abundance: int = 100,
    abundance_fraction: float = 0.001,
    flip: bool = False,
    denoise: str = "-",
    unoise_alpha: Optional[float] = None,
    unoise_gamma: Optional[int] = None,
    cpu: int = 1,
    debug: bool = False,
) -> (BIOMV210Format, DNAFASTAFormat):
    """THAPBI PICT's prepare-reads and sample-tally.

    Starts by making a temporary workind directory. Into this it creates a
    ``raw_data/`` folder of symlinks using ``<SAMPLE>_R1.fastq.gz`` and
    ``<SAMPLE>_R2.fastq.gz`` naming based on the QZA file manifest. Then takes
    the given primer definitations, and sets up a dummy THAPBI PICT database
    using those but no reference sequences.

    The other parameters are passed to THAPBI PICT ``prepare-reads`` and
    ``sample-tally`` as they are.
    """
    cpu = check_cpu(cpu)

    tmp_obj = tempfile.TemporaryDirectory()
    tmp_dir = tmp_obj.name

    # Setup the FASTQ inputs (could extend to multiple QZA files...)
    raw_data = os.path.join(tmp_dir, "raw_data")
    os.mkdir(raw_data)
    for key, qza in demultiplexed_seqs.items():
        # Give each QZA file its own subdirectory (and thus pool
        # if we can later apply control driven abundance thresholds)
        qza_pool = os.path.join(tmp_dir, "raw_data", str(key))
        os.mkdir(qza_pool)
        setup_rawdata(str(qza), qza_pool, debug=debug)

    # Setup the dummy THAPBI PICT database
    db_filename = os.path.join(tmp_dir, "primers.sqlite")
    db_url = "sqlite:///" + db_filename
    markers = setup_marker(db_url, primer_definition, debug=debug)
    session = connect_to_db(db_url)()

    # Call THAPBI PICT prepare-reads
    out_dir = os.path.join(tmp_dir, "intermediate")
    os.mkdir(out_dir)
    if debug:
        sys.stderr.write("DEBUG: Now starting THAPBI PICT prepare-reads\n")
    fasta_list = prepare_reads(
        fastq=[raw_data],
        out_dir=out_dir,
        session=session,
        flip=flip,
        min_abundance=abundance,
        min_abundance_fraction=abundance_fraction,
        ignore_prefixes=None,
        merged_cache=None,
        tmp_dir=tmp_dir,
        debug=debug,
        cpu=cpu,
    )
    if debug:
        sys.stderr.write(f"DEBUG: Have {len(fasta_list)} intermediate FASTA files\n")

    biom_out_dict = {}
    fasta_out_dict = {}

    # Call THAPBI PICT sample-tally
    for marker in markers:
        if debug:
            sys.stderr.write(
                f"DEBUG: Now starting THAPBI PICT sample-tally for {marker}\n"
            )

        tally_out = os.path.join(tmp_dir, marker + ".tally.tsv")
        biom_out = BIOMV210Format()
        fasta_out = DNAFASTAFormat()

        sample_tally(
            inputs=[
                _ for _ in fasta_list if _.startswith(os.path.join(out_dir, marker))
            ],
            synthetic_controls=[],
            negative_controls=[],
            output=tally_out,
            session=session,
            marker=marker,
            spike_genus="",
            min_abundance=abundance,
            min_abundance_fraction=abundance_fraction,
            # Match current THAPBI PICT pipeline behaviour:
            total_min_abundance=abundance,
            denoise_algorithm=denoise,
            unoise_alpha=unoise_alpha,
            unoise_gamma=unoise_gamma,
            biom=str(biom_out),
            fasta=str(fasta_out),
            tmp_dir=tmp_dir,
            debug=debug,
            cpu=cpu,
        )

        # Turn this into a dict for the output Collection
        biom_out_dict[marker] = biom_out
        fasta_out_dict[marker] = fasta_out
    session.close()

    if debug:
        sys.stderr.write(f"DEBUG: Removing q2-thapbi-pict temp folder {tmp_dir}\n")
    tmp_obj.cleanup()

    return biom_out_dict, fasta_out_dict
