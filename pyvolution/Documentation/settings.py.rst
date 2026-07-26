settings.py
***********

Since a run of evolution needs many coordinated settings, this file is where those
settings are assembled, one function per problem, into the single
``argparse.Namespace`` that :func:`GA.runGA` expects.

getOneMaxSettings()
=====================

.. function:: getOneMaxSettings()

   :rtype: argparse.Namespace with ``.func`` and ``.args`` attributes

The only complete, working settings function in this file. Builds the settings for
solving the One-Max problem (maximize the number of ``'1'`` genes in a 30-gene binary
chromosome, population of 1000, over up to 100 generations or until a score of 30 is
reached) and returns them wrapped for :func:`GA.py`'s ``__main__`` block:
the returned ``argparse.Namespace`` has ``.func`` set to :func:`GA.runGA` and ``.args``
set to the actual settings namespace described below, so that it's called as
``result.func(result.args)``.

Fields of the settings namespace (``result.args``)
=====================================================

There are no default values in this framework, by design -- every field below must be
set explicitly.

``genfunc`` / ``genparams``
-----------------------------
``genfunc`` generates the initial population, called as ``genfunc(genparams)``. In
``getOneMaxSettings``, this is :func:`population.genPop`, and ``genparams`` is itself a
namespace with:

- ``genparams.popSize`` -- the number of individuals in the population
- ``genparams.chromGens`` -- a list of ``(function, params)`` tuples, one per
  chromosome (see :doc:`population.py`)

``maxGens``
------------
The maximum number of generations for which evolution shall run, after which it stops even if no individual has reached ``targetscore``.

``targetscore``
-----------------
The fitness score at which evolution stops early, once reached.

``SCORES``
-----------
A dictionary that memoizes the fitness values of individuals already scored. Usually starts as an empty dict, and is shared by reference into ``scoreparams``/``selectparams`` below.

``scorefunc`` / ``scoreparams``
----------------------------------
``scorefunc`` evaluates an individual's fitness, called as ``scorefunc(scoreparams)``.
In ``getOneMaxSettings``, this is :func:`fitness.score`, and ``scoreparams`` is a
namespace with:

- ``scoreparams.scorefuncs`` -- a list of ``(function, params)`` tuples, one per
  chromosome (see :doc:`fitness.py`)
- ``scoreparams.SCORES`` -- the same dict as the top-level ``SCORES``

.. note::

    The individual being scored is not part of ``scoreparams`` at settings-construction
    time -- :func:`fitness.score` sets ``scoreparams.individual``/``.chrom`` itself for
    each call, since which individual is being scored can only be known once evolution
    is running.

``selectfunc`` / ``selectparams``
------------------------------------
``selectfunc`` chooses individuals for reproduction, called as
``selectfunc(selectparams)``. In ``getOneMaxSettings``, this is
:func:`selection.rouletteWheelSelect`, and ``selectparams`` carries ``.SCORES``,
``.scorefunc``, and ``.scoreparams`` through to it. As with scoring, the population to
select from is supplied by :func:`GA.runGA` itself at call time, not baked into these
settings.

``getWheel``
-------------
A ``bool``, computed automatically as ``selectfunc in {selection.rouletteWheelSelect}``, indicating whether :func:`GA.runGA` must (re)compute a roulette wheel each generation before calling ``selectfunc``.

``crossfunc`` / ``crossparams`` / ``crossprob``
--------------------------------------------------
``crossfunc`` combines two parents into children, called as ``crossfunc(crossparams)``.
In ``getOneMaxSettings``, this is :func:`crossover.twoChildCrossover`, and
``crossparams`` is a namespace whose own ``.crossparams`` attribute is a list of
``(function, params)`` tuples, one per chromosome (see :doc:`crossover.py`).
``crossprob`` is the probability, in ``[0, 1]``, that a given pair of selected parents
is actually crossed over.

``mutfunc`` / ``mutparams`` / ``mutprob``
--------------------------------------------
``mutfunc`` mutates a single child, called as ``mutfunc(mutparams)``. In
``getOneMaxSettings``, this is :func:`mutation.mutateSingleAllele`, and ``mutparams``
carries ``.chrom`` (which chromosome to mutate) and ``.chars`` (the allowed alphabet,
reused from the chromosome-generation params). ``mutprob`` is the probability, in
``[0, 1]``, that a given child is mutated.

``numCrossOvers``
-------------------
How many crossover operations :func:`GA.runGA` attempts per generation.

.. note::

    Traveling Salesman Problem (TSP) support is currently partial/removed. This file
    used to contain a second settings function for TSP (wiring together
    :func:`population.genTour`, :func:`fitness.scoreTSP`, :func:`crossover.injectionco`,
    and PyGame-based visualization); that function's entire body is now commented out,
    and the ``visualization.py`` module it depended on no longer exists in this
    repository. See the top-level README's Known Issues.
