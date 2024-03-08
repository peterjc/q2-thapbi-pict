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


Release process
---------------

Pending.
