# Pyvolution

Pyvolution is a general-purpose evolutionary algorithms framework for Python. It provides
the building blocks of a genetic algorithm — individuals, population generation, fitness
evaluation, selection, crossover, and mutation — as independent, composable modules, plus
a driver (`GA.py`) that wires them together and runs the evolution loop.

The framework uses [pystitia](https://github.com/inspectorG4dget/pystitia) for
Design by Contract: most public functions declare their pre/postconditions directly in
code via a `@contracts(...)` decorator, which can be toggled on and off with a
`__testmode__` flag.

## Installation

Pyvolution requires **Python 3.7+**.

1. Install the dependencies:

   ```bash
   pip install pystitia tqdm colorama
   ```

2. Add the package's source directory to your `PYTHONPATH`:

   ```bash
   export PYTHONPATH="$PYTHONPATH:/path/to/Genetic-Framework/pyvolution/pyvolution"
   ```

   This step is required and is **not** the same as a normal `pip install .` of the
   package. The modules import each other with bare, top-level imports (e.g.
   `from individual import Individual` rather than a relative import), so they only
   resolve correctly when `pyvolution/pyvolution` itself — not its parent — is on the
   import path. See [Known Issues](#known-issues).

See [Required Installs](pyvolution/Documentation/Required%20Installs.rst) for more detail.

## Overview

A run of evolution is configured entirely through a single `argparse.Namespace` of
settings (see `settings.py` for a worked example, `getOneMaxSettings`), which specifies:

- **`genfunc`** / **`genparams`** — how to generate the initial population (`population.py`)
- **`scorefunc`** / **`scoreparams`** — how to evaluate an individual's fitness (`fitness.py`)
- **`selectfunc`** / **`selectparams`** — how individuals are chosen for reproduction (`selection.py`)
- **`crossfunc`** / **`crossparams`** — how two parents combine to produce children (`crossover.py`)
- **`mutfunc`** / **`mutparams`** — how a child may be mutated (`mutation.py`)

Every function across these modules takes a single `args` (`argparse.Namespace`) object
rather than positional parameters, so that settings can be composed and passed around
uniformly. `GA.py`'s `runGA` is the driver that consumes this settings object and runs
the generational loop, dispatching crossover/mutation work to worker processes defined
in `parallel.py`.

`individual.py` defines the `Individual` class: a wrapper around an ordered list of
chromosomes, with the identity/equality/hashing semantics the rest of the framework
relies on (e.g. population uniqueness).

Full per-module API reference is in the [Sphinx documentation](pyvolution/Documentation/index.rst).

## Known Issues

- **`GA.runGA` currently crashes at runtime.** It contains an invalid expression
  (`[p for p in pop in p not in SCORES]`) that raises `NameError` as soon as it's
  called, and it also does `import sanity` / calls `sanity.sanity(args)` for a
  `sanity` module that does not exist anywhere in this repository. There is currently
  no way to run a full evolution end-to-end.
- **The TSP example is incomplete.** `settings.py`'s `getTSPSettings` (the settings
  needed to run the Traveling Salesman Problem example) is entirely commented out, and
  the `visualization.py` module it depended on for drawing the tour has been removed.
  `fitness.scoreTSP`, `crossover.injectionco`, and the `berlin52.txt` city-coordinate
  data file still exist as working code/data, but nothing currently wires them together.

## License

Apache License, Version 2.0. See `pyvolution/pyvolution/LICENSE.txt` and `NOTICE.txt`.
