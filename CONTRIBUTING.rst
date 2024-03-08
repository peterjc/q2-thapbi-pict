Development Notes
=================

Python style conventions
------------------------

The plugin follows the same conventions as the main THAPBI PICT tool,
PEP8 and black style enforced via pre-commit. Install these tools using:

.. code:: console

    $ pip install pre-commit
    $ pre-commit install  # within the q2-thapbi-pict main directory

The checks will then run automatically when you make a git commit. You can
also run the checks directly using:

.. code:: console

    $ pre-commit run -a

If your editor can be configured to run flake8 and/or ruff automatically,
even better. These checks are done as part of the continuous integration when
changes are made on GitHub.


Continuous Integration
----------------------

Pending.


Installing from source
----------------------

First, download the code from GitHub and decompress it if required. The best
way to do this if you are likely to contribute any changes is at the command
line with ``git``. Then run the pip install command in developer mode:

.. code:: console

    $ git clone https://github.com/peterjc/q2-thapbi-pict.git
    $ cd q2-thapbi-pict
    $ pip install -e .  # assuming qiime2 conda env is active!

If you change the plugin's interface to Qiime2, you need to run this:

.. code:: console

    $ qiime dev refresh-cache

Otherwise changes to the plugin code take effect next time it is used.


Release process
---------------

Pending.
