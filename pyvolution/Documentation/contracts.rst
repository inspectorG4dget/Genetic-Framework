Contracts
**********

This framework uses `pystitia <https://github.com/inspectorG4dget/pystitia>`_ for
Design by Contract: functions are wrapped in ``@contracts(preconditions=(...),
postconditions=(...))``, where each condition is a lambda that pystitia calls with
whichever of the function's ``args`` attributes (or, for postconditions,
``__return__``/``__old__``) it asks for by name. These checks only run when the
module-level ``__testmode__`` flag is ``True`` (via ``pystitia.setTestMode``); this
page summarizes, in plain language, the contracts declared in the source today.

.. note::

    The contracts themselves live in the source as the single source of truth (next to
    the function they describe). This page is a curated summary for readability, kept
    in sync with the source -- if the two disagree, trust the source.

individual.py
=============

``Individual.__init__(self, chromosomes)``
--------------------------------------------

Preconditions
+++++++++++++
1. ``chromosomes`` is a ``list``

Postconditions
+++++++++++++++
1. ``self.chromosomes`` exists

``Individual.__eq__(self, other)``
------------------------------------

Preconditions
+++++++++++++
1. ``other`` is an instance of :class:`Individual`

Postconditions
+++++++++++++++
1. Neither ``self`` nor ``other`` is changed

``Individual.__hash__(self)``
--------------------------------

Postconditions
+++++++++++++++
1. ``self`` is not changed

``Individual.__len__(self, chrom=None)``
-------------------------------------------

Preconditions
+++++++++++++
1. If ``chrom`` is given, it is a valid index (positive, in range, or the equivalent negative index)

Postconditions
+++++++++++++++
1. ``self`` is not changed

``Individual.__getitem__(self, i)``
--------------------------------------

Preconditions
+++++++++++++
1. ``i`` is a valid index (positive, in range, or the equivalent negative index)

Postconditions
+++++++++++++++
1. ``self`` is not changed

``Individual.__setitem__(self, index, obj)``
-----------------------------------------------

Preconditions
+++++++++++++
1. ``index`` is a valid index (positive, in range, or the equivalent negative index)

Postconditions
+++++++++++++++
1. ``self.chromosomes[index]`` is ``obj``

``Individual.__contains__(self, chromosome)``
------------------------------------------------

Postconditions
+++++++++++++++
1. Neither ``self`` nor ``chromosome`` is changed

``Individual.__repr__(self)`` / ``Individual.__str__(self)``
----------------------------------------------------------------

Postconditions
+++++++++++++++
1. ``self`` is not changed

``Individual.append(self, chrom)``
--------------------------------------

Postconditions
+++++++++++++++
1. ``len(self.chromosomes)`` increases by exactly 1
2. The last chromosome in ``self.chromosomes`` is ``chrom``

``Individual.count(self, sub, chrom)``
------------------------------------------

Postconditions
+++++++++++++++
1. ``self.chromosomes`` is not changed

population.py
==============

``genPop(args)``
-------------------

Preconditions
+++++++++++++
1. ``args.popSize > 0``
2. ``args.chromGens`` is a list of ``(callable, argparse.Namespace)`` tuples

Postconditions
+++++++++++++++
1. ``args.chromGens`` is not changed
2. Returns a list of length ``args.popSize``
3. Every individual in the returned list is unique

``genCharsChrom(args)``
--------------------------

Preconditions
+++++++++++++
1. ``args.numGenes`` is an ``int``
2. ``args.bases`` supports ``__getitem__``/``__len__`` and is non-empty

Postconditions
+++++++++++++++
1. ``args.numGenes``/``args.bases`` are not changed
2. Returns a list of length ``args.numGenes``
3. Every element of the returned list is drawn from ``args.bases``

``genTour(args)``
--------------------

Preconditions
+++++++++++++
1. ``args.numCities`` is an ``int``

Postconditions
+++++++++++++++
1. ``args.numCities`` is not changed
2. Returns a list of length ``args.numCities``
3. The returned list is a permutation of ``range(args.numCities)``

fitness.py
===========

``score(args)``
------------------

Preconditions
+++++++++++++
1. ``args.individual`` is an :class:`individual.Individual`
2. ``args.scorefuncs`` is a list of ``(callable, tuple)`` pairs
3. ``args.SCORES`` is a ``dict``

Postconditions
+++++++++++++++
1. ``args.individual`` is not changed
2. ``args.individual`` is a key in ``args.SCORES`` afterwards
3. If ``args.individual`` was already in ``args.SCORES``, its size is unchanged; otherwise it grows by exactly 1

``scoreOnes(args)``
----------------------

Preconditions
+++++++++++++
1. ``args.individual`` is an :class:`individual.Individual`
2. Every chromosome of ``args.individual`` is a list
3. Every gene in chromosome 0 is ``'0'`` or ``'1'``

Postconditions
+++++++++++++++
1. ``args.individual`` is not changed
2. Returns an ``int >= 0``

``scoreTSP(args)``
---------------------

Preconditions
+++++++++++++
1. ``args.tour`` is a list of ``int``
2. ``args.DIST`` is a ``dict`` of ``{int: {int: float}}``

Postconditions
+++++++++++++++
1. Returns a ``float``
2. ``args.tour``/``args.DIST`` are not changed

selection.py
=============

``getRouletteWheel(args)``
-----------------------------

Preconditions
+++++++++++++
1. ``args.pop`` is a list of :class:`individual.Individual`
2. ``args.SCORES`` is a dict keyed by every individual in ``args.pop``

Postconditions
+++++++++++++++
1. ``args.pop`` is not changed
2. Returns a list of 3-tuples ``(individual, low, high)``, one per individual in ``args.pop``, with ``low <= high``

``rouletteWheelSelect(args)``
--------------------------------

Preconditions
+++++++++++++
1. ``args.wheel`` is a list of valid 3-tuples, as returned by ``getRouletteWheel``
2. ``args.s`` (if present) is a ``float`` or ``None``

Postconditions
+++++++++++++++
1. ``args.wheel`` is not changed
2. Returns an :class:`individual.Individual`

``tournamentSelect(args)``
-----------------------------

Preconditions
+++++++++++++
1. ``args.population`` is a list of :class:`individual.Individual`
2. ``args.T``, ``args.w``, ``args.n`` are ``int``, with ``w <= n``, ``n % w == 0``, ``w <= T``, ``len(pop) >= T``, ``T >= n``
3. ``args.scoreparams`` is a ``tuple``

Postconditions
+++++++++++++++
1. ``args.population``/``args.T``/``args.w``/``args.n``/``args.scorefunc``/``args.scoreparams`` are not changed
2. Returns a list of ``args.n`` individuals

.. note::

    The preconditions for ``tournamentSelect`` check ``args.population`` in one clause
    and ``args.pop`` in another -- these are two different attribute names on the same
    ``args`` object. This is an inconsistency in the current source (see the module
    itself), not a documentation choice; both attributes must be supplied for the
    contract checks to pass in test mode.

crossover.py
=============

``crossOnes(args)``
----------------------

Preconditions
+++++++++++++
1. ``args.p1`` and ``args.p2`` are ``list``

Postconditions
+++++++++++++++
1. ``args.p1``/``args.p2`` are not changed
2. Returns a 2-tuple of new lists (not the same objects as the inputs)

``injectionco(args)``
------------------------

Preconditions
+++++++++++++
1. ``args.p1`` and ``args.p2`` are equal-length lists, each a permutation of ``range(len(args.p1))``

Postconditions
+++++++++++++++
1. ``args.p1``/``args.p2`` are not changed
2. Returns a new list of the same length, containing exactly the same elements as ``args.p1`` (and ``args.p2``), each exactly once

``twoChildCrossover(args)``
------------------------------

Preconditions
+++++++++++++
1. Every entry in ``args.crossparams`` is a ``tuple``

Postconditions
+++++++++++++++
1. Returns a 2-tuple of :class:`individual.Individual`

``oneChildCrossover(args)``
------------------------------

Preconditions
+++++++++++++
1. ``args.p1``/``args.p2`` are :class:`individual.Individual` of equal length
2. ``len(args.crossfuncs) == len(args.p1) == len(args.crossparams)``

Postconditions
+++++++++++++++
1. ``args.p1``/``args.p2`` are not changed
2. Returns a single :class:`individual.Individual` whose chromosome lengths match the parents'

mutation.py
============

``mutateSingleAllele(args)``
-------------------------------

Preconditions
+++++++++++++
1. ``args.individual`` is an :class:`individual.Individual`
2. ``args.chrom`` is a valid chromosome index

Postconditions
+++++++++++++++
1. ``args.individual``/``args.chrom`` are not changed
2. Returns a different (by identity and by value) :class:`individual.Individual`
3. Every gene in the mutated chromosome comes from ``args.chars``
4. Every other chromosome is unchanged

``swapmut(args)`` / ``revmut(args)`` / ``shufflemut(args)``
----------------------------------------------------------------

Preconditions
+++++++++++++
1. ``args.p`` is an :class:`individual.Individual`
2. ``args.chrom`` is a valid chromosome index

Postconditions
+++++++++++++++
1. ``args.p``/``args.chrom`` are not changed
2. Returns an :class:`individual.Individual` whose ``args.chrom``\\ th chromosome contains the same genes as ``args.p``'s, in a different order (or, for ``shufflemut``/``swapmut``, differing in at least the genes that were swapped/shuffled)

GA.py
======

``runGA(args)``
-------------------

Preconditions
+++++++++++++
1. ``sanity.sanity(args)`` passes
2. ``args.maxGens > 0``

Postconditions
+++++++++++++++
1. ``args`` is not changed
2. The returned fittest score is ``>= args.targetscore``, or the returned generation count is ``>= args.maxGens``
3. The returned fittest individual is an :class:`individual.Individual`

.. warning::

    The first precondition, ``sanity.sanity(args)``, can never pass: no ``sanity``
    module exists anywhere in this repository, so evaluating this precondition raises
    ``ImportError``/``ModuleNotFoundError`` rather than returning ``True`` or ``False``.
    Combined with the runtime bug described in :doc:`GA.py`, ``runGA`` cannot currently
    be run to completion even with ``__testmode__`` off. See the top-level README's
    Known Issues.
