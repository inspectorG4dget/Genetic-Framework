Required Installations
**********************

Python 3.7+
===========

This package requires Python 3.7 or later.

pystitia
========

Used for Design by Contract checking (enforced when ``__testmode__`` is ``True``; see
the documentation for :doc:`settings.py`). Install with ``pip install pystitia``. See
the `pystitia repository <https://github.com/inspectorG4dget/pystitia>`_ for details on
how contracts are declared and enforced.

tqdm
====

Used to display progress bars during evolution (population fitness scoring, generation
progress, etc). Install with ``pip install tqdm``.

colorama
========

Declared as a dependency of the package (used transitively by ``tqdm`` for colored
terminal output on some platforms). Install with ``pip install colorama``.

PYTHONPATH
==========

The modules in this package import each other with bare, top-level imports (e.g.
``from individual import Individual``) rather than relative imports. As a result, the
directory containing the source files -- ``pyvolution/pyvolution`` -- must itself be on
``sys.path`` (for example via ``PYTHONPATH``, or by running scripts from within that
directory). A normal ``pip install`` of the package followed by ``import
pyvolution.something`` will raise ``ModuleNotFoundError`` for these sibling imports. See
the top-level README's Installation section for the concrete steps.

Building this documentation
============================

To build these docs yourself, you additionally need ``sphinx`` and
``sphinx_rtd_theme``:

.. code-block:: bash

    pip install sphinx sphinx_rtd_theme
    cd pyvolution/Documentation
    make html
