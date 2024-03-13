.. image:: https://img.shields.io/github/license/peterjc/q2-thapbi-pict.svg?label=License
   :alt: MIT License
   :target: https://github.com/peterjc/q2-thapbi-pict/blob/main/LICENSE.rst
.. image:: https://results.pre-commit.ci/badge/github/peterjc/q2-thapbi-pict/main.svg
   :target: https://results.pre-commit.ci/latest/github/peterjc/q2-thapbi-pict/main
   :alt: pre-commit.ci status
.. image:: https://img.shields.io/pypi/v/q2_thapbi_pict.svg?label=PyPI
   :alt: Released on the Python Package Index (PyPI)
   :target: https://pypi.org/project/q2-thapbi-pict/
.. image:: https://img.shields.io/badge/Code%20style-black-000000.svg
   :alt: Code style: black
   :target: https://github.com/python/black


Qiime2 plugin for THAPBI PICT (q2-thapbi-pict)
==============================================

About
-----

`Qiime2 <https://qiime2.org/>`__ is a microbiome bioinformatics platform with
integrated data provenance tracking and a `plugin system
<https://library.qiime2.org/plugins/>`__ allowing modular construction of
analysis and visualisation pipelines.

`THAPBI PICT <https://github.com/peterjc/thapbi-pict>`__ is a sequence based
diagnostic/profiling tool started under the UK funded Tree Health and Plant
Biosecurity Initiative (THAPBI) `Phyto-Threats project
<https://www.forestresearch.gov.uk/research/global-threats-from-phytophthora-spp/>`__.
PICT stood for *Phytophthora* ITS1 Classification Tool, reflecting the initial
application focus.

With appropriate primer settings and a custom database of full length markers,
THAPBI PICT can be applied to other organisms and/or barcode marker sequences.
It requires overlapping paired-end Illumina reads which can be merged to cover
the *full* amplicon marker. Longer markers or fragmented amplicons are not
supported. Internally it works by tracking unique amplicon sequence variants
(ASVs), using MD5 checksums as identifiers.

The THAPBI PICT tool provides a command line interface including a pipeline
from demultiplexed FASTQ files and optional metadata as TSV files though to
ASV tally tables with taxonomic classification as TSV, Excel or BIOM files.

This repository is for ``q2-thapbi-pict``, a plugin to call some of the THAPBI
PICT functionality from within Qiime2.


Installation
------------

Qiime2 is not available natively on Windows, instead they recommend using the
Windows Subsystem for Linux (WSL). Follow the Qiime2 installation instructions
using the `Conda <https://conda.io/>`__ packaging system.

1. Activate your Qiime2 conda environment.

2. Install the paired read merging tool Flash used by THAPBI PICT using conda:

   .. code:: console

        $ conda install -c conda-forge flash

3. Install the THAPBI PICT plugin for Qiime2 (and its Python dependencies which
   include THAPBI PICT and CutAdapt) using pip:

   .. code:: console

        $ pip install q2-thapbi-pict

   This will fail ``ERROR: No matching distribution found for q2-types...`` or
   ``ERROR: No matching distribution found for q2cli...`` if the Qiime2 conda
   environment is not activated.

Quick Start
-----------

Once installed, you should be able to run the tool at the command line using
the Qiime2 command line interface (q2cli):

.. code:: console

    $ qiime info
    System versions
    Python version: 3.8.18
    QIIME 2 release: 2024.2
    QIIME 2 version: 2024.2.0
    q2cli version: 2024.2.0

    Installed plugins
    ...

This should list the THAPBI PICT plugin under "Installed plugins". You should
be able to run it and see basic instructions too:

.. code:: console

    $ qiime q2-thapbi-pict --help
    Usage: qiime q2-thapbi-pict [OPTIONS] COMMAND [ARGS]...

      Description: This QIIME 2 plugin provides support for running some of the
      THAPBI PICT functionality.

    ...

This lists the available commands, each of which have their own help page:

.. code:: console

    $ qiime q2-thapbi-pict prepare-reads-sample-tally --help
    Usage: qiime q2-thapbi-pict prepare-reads-sample-tally [OPTIONS]

      Takes paired (raw) FASTQ files demultiplexed per sample. Runs THAPBI PICT
      ...

You can confirm the plugin version like this:

.. code:: console

    $ qiime q2-thapbi-pict --version
    QIIME 2 Plugin 'q2-thapbi-pict' version 0.0.1 (from package 'q2-thapbi-pict' version 0.0.1)


Documentation
-------------

The `THAPBI PICT documentation <https://thapbi-pict.readthedocs.io/>`_ is
hosted by `Read The Docs <https://readthedocs.org/>`_.


Citation
--------

If you use THAPBI PICT in your work, please cite our *PeerJ* paper, and give
details of the version and any non-default settings used in your methods:

    Cock *et al.* (2023) "THAPBI PICT - a fast, cautious, and accurate
    metabarcoding analysis pipeline" *PeerJ* **11**:e15648
    https://doi.org/10.7717/peerj.15648

You can also cite the software specifically via Zenodo which offers version
specific DOIs as well as https://doi.org/10.5281/zenodo.4529395 which is for
the latest version.

Qiime2 helps by tracking the citations for all the tools your analysis uses.
This should include any tools used via plugins, such as Flash and CutAdapt.
