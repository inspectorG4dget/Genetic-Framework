Overview - How to use this Framework
*************************************

Pyvolution builds an evolutionary algorithm out of independent, swappable pieces:
population generation, fitness evaluation, selection, crossover, and mutation. A run of
evolution is configured by building a single ``argparse.Namespace`` of settings (see
:doc:`settings.py`, and in particular ``getOneMaxSettings``, for a complete worked
example) and handing it to :func:`GA.runGA`.

The ``args`` calling convention
================================

Every public function in this framework takes exactly one argument: an
``argparse.Namespace`` conventionally named ``args``, whose attributes are that
function's "real" parameters. For example, :func:`population.genPop` is conceptually
``genPop(N, chromGenfuncs, chromGenParams)``, but is actually called as
``genPop(args)`` where ``args.popSize`` and ``args.chromGens`` hold those values.

This convention lets settings be built up, nested, and passed around uniformly (a
``Namespace`` of settings can itself contain other ``Namespace``\\ s for the functions
it configures), and gives :func:`pystitia.contracts` (see below) a single, consistent
way to inspect a function's inputs.

Design by Contract with pystitia
==================================

Most functions are decorated with ``@contracts(preconditions=(...),
postconditions=(...))`` from the `pystitia <https://github.com/inspectorG4dget/pystitia>`_
package. Each precondition/postcondition is a lambda naming the ``args`` attributes (or
``__return__``/``__old__`` for postconditions) it needs to check. These checks only run
when the module-level ``__testmode__`` flag is ``True`` (set via
``pystitia.setTestMode``) -- this is a runtime cost you can turn off outside of
development/debugging. See :doc:`contracts` for a summary of the contracts declared by
each function.

individual.py
==============
This file defines what an individual is (in a class). Generically, an :class:`individual.Individual` is simply an ordered collection of chromosomes, held in a ``list`` (as opposed to a ``set``), since each chromosome plays a distinct role for a given problem.

Also implemented in this file are the methods that give ``Individual`` value semantics: ``__hash__`` and ``__eq__`` (based on the chromosomes themselves), ``__len__``, ``__getitem__``/``__setitem__``, ``__contains__``, and ``__repr__``.

population.py
==============
This file contains the functions that define population generation. The important function defined here is :func:`population.genPop`, which may be used as an interface to creating a population of unique individuals.

``genPop(args)`` expects ``args.popSize`` (the number of individuals to generate) and ``args.chromGens``: a list of ``(function, params)`` tuples, one per chromosome. The ``i``\\ th tuple's function is called as ``func(params)`` to generate the ``i``\\ th chromosome of each individual.

.. note::

    Because :func:`population.genPop` uses a ``set`` internally to guarantee uniqueness before returning a list, :class:`individual.Individual` must implement a meaningful ``__hash__`` (it does, based on its chromosomes).

Two chromosome-generation helpers are also provided: :func:`population.genCharsChrom` (a chromosome of random characters from an alphabet -- used by the One-Max example) and :func:`population.genTour` (a random permutation of city indices -- for the Traveling Salesman Problem; see the note on TSP below).

fitness.py
==========
This file contains the machinery for evaluating the fitness of an individual, plus a couple of concrete scoring functions. The main function is :func:`fitness.score`.

``score(args)`` expects ``args.individual``, ``args.scorefuncs`` (a list of ``(function, params)`` tuples -- one per chromosome), and ``args.SCORES`` (a dict caching individual -> fitness). It sums the per-chromosome scores and memoizes the result in ``SCORES``.

.. note::

    If ``args.individual`` was not already a key in ``args.SCORES``, :func:`fitness.score` inserts it. ``SCORES`` is therefore modified in place as a side effect.

Two chromosome scoring functions are included: :func:`fitness.scoreOnes` (counts ``'1'`` genes -- the One-Max problem) and :func:`fitness.scoreTSP` (total tour distance, given a distance dictionary -- for TSP; see the note on TSP below).

selection.py
=============
This file contains the functions used to select individuals from a population.

There are three functions implemented:

1. :func:`selection.getRouletteWheel`
2. :func:`selection.rouletteWheelSelect`
3. :func:`selection.tournamentSelect`

:func:`selection.getRouletteWheel`
------------------------------------
Builds a fitness-proportional roulette wheel from ``args.pop`` (a list of individuals) and ``args.SCORES``: a list of 3-tuples ``(individual, low, high)`` where ``individual`` "owns" the ``[low, high)`` section of the ``[0, 1)`` wheel, proportional to its fitness.

:func:`selection.rouletteWheelSelect`
----------------------------------------
Given ``args.wheel`` (as produced by ``getRouletteWheel``) and optionally ``args.s`` (a float in ``[0, 1)``; a random one is chosen if not supplied), performs a binary search over the wheel and returns the individual whose section contains ``s``.

:func:`selection.tournamentSelect`
-------------------------------------
Given ``args.population``, tournament size ``args.tournsize``, number of winners per tournament ``args.numwinners``, number to select ``args.numselect``, and a scoring function/params, repeatedly samples tournaments of ``args.tournsize`` individuals and keeps the fittest ``args.numwinners`` from each, until ``args.numselect`` individuals have been collected.

crossover.py
=============

Functions that cross over chromosomes (or whole individuals) between two parents. There is no single generic driver function here, since which crossover to use is a per-problem choice made in ``settings.py``.

- :func:`crossover.crossOnes` -- single-point crossover of two chromosomes (lists), returning two children.
- :func:`crossover.injectionco` -- order-preserving crossover for permutation-encoded chromosomes (e.g. TSP tours), returning one child.
- :func:`crossover.twoChildCrossover` / :func:`crossover.oneChildCrossover` -- drive crossover across *all* chromosomes of two :class:`individual.Individual` parents (using the per-chromosome crossover functions/params in ``args.crossfuncs``/``args.crossparams``), returning two children or one, respectively.

mutation.py
============

Functions that mutate a single chromosome of an individual, always returning a *new* ``Individual`` rather than mutating in place.

- :func:`mutation.mutateSingleAllele` -- replaces one random gene with a different value from ``args.chars``.
- :func:`mutation.swapmut` -- swaps two random genes.
- :func:`mutation.revmut` -- reverses the genes between two random points.
- :func:`mutation.shufflemut` -- shuffles the chromosome with ``random.shuffle``.

GA.py
======

:func:`GA.runGA` is the main driver: given the full settings ``args``, it generates the initial population, scores it (dispatching fitness evaluation across a process pool), then repeatedly selects parents, crosses them over, mutates the children, and rescores, until either ``args.targetscore`` is reached or ``args.maxGens`` generations have elapsed. Crossover and mutation work for each generation is queued to worker processes defined in :doc:`parallel.py`.

.. warning::

    ``GA.runGA`` currently raises ``NameError`` immediately when called, and also
    depends on an ``import sanity`` module that does not exist in this repository. See
    the top-level README's Known Issues section. This is a real bug in the code, not a
    documentation gap.

settings.py
============

Since a run of evolution needs many coordinated settings, this file is where those settings are assembled into a single ``argparse.Namespace``, one function per problem. :func:`settings.getOneMaxSettings` is the complete, working example: it wires together :func:`population.genPop` (with :func:`population.genCharsChrom`), :func:`fitness.score` (with :func:`fitness.scoreOnes`), :func:`selection.rouletteWheelSelect`, :func:`crossover.twoChildCrossover` (with :func:`crossover.crossOnes`), and :func:`mutation.mutateSingleAllele` to solve the One-Max problem.

A second function, for the Traveling Salesman Problem, exists only as commented-out code in this file (see the note on TSP below).

.. note::

    Traveling Salesman Problem (TSP) support is currently partial/removed. The
    TSP-specific settings function is entirely commented out, and the ``visualization.py``
    module it depended on (for drawing tours with PyGame) no longer exists in this
    repository. The lower-level pieces -- :func:`fitness.scoreTSP`,
    :func:`crossover.injectionco`, :func:`population.genTour`, and the ``berlin52.txt``
    city-coordinate data file -- are still present and functional as building blocks,
    but nothing currently assembles them into a runnable example.
