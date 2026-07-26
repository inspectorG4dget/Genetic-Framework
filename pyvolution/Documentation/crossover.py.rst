crossover.py
************

crossOnes(args)
================

.. function:: crossOnes(args)

   :param args.p1: the first parent chromosome
   :type args.p1: list
   :param args.p2: the second parent chromosome
   :type args.p2: list
   :rtype: tuple of two new child chromosomes (lists)

Length-preserving single-point crossover of two chromosomes. A crossover point is chosen at random; the two children are the two ways of splicing ``args.p1``/``args.p2`` at that point.

injectionco(args)
==================

.. function:: injectionco(args)

   :param args.p1: the first parent chromosome -- a permutation of ``range(len(args.p1))``
   :type args.p1: list of int
   :param args.p2: the second parent chromosome -- a permutation of ``range(len(args.p2))``, same length as ``args.p1``
   :type args.p2: list of int
   :rtype: a single child chromosome (list) -- also a permutation

Order-preserving crossover for permutation-encoded chromosomes (e.g. TSP tours), performed as follows:

1. Select distinct points A < B between 0 and ``len(args.p1)``.
2. Make an empty child chromosome of length ``len(args.p1)``.
3. Copy the genes of ``args.p1`` from A to (but not including) B into the corresponding positions of the child.
4. Fill in the rest of the child's genes with the genes from ``args.p2``, in the order they appear in ``args.p2``, skipping any allele already placed in the child.

Return the child chromosome.

twoChildCrossover(args)
========================

.. function:: twoChildCrossover(args)

   :param args.p1: the first parent
   :type args.p1: instance of :class:`individual.Individual`
   :param args.p2: the second parent, with the same number of chromosomes as ``args.p1``
   :type args.p2: instance of :class:`individual.Individual`
   :param args.crossparams: a list of ``(function, params)`` tuples, one per chromosome. The ``i``\\ th function is called with a fresh ``argparse.Namespace`` whose ``p1``/``p2`` attributes are set to the ``i``\\ th chromosome of ``args.p1``/``args.p2``, and is assumed to return a 2-tuple of child chromosomes
   :type args.crossparams: list of (function, argparse.Namespace) tuples
   :rtype: tuple of two :class:`individual.Individual` children

Cross over all chromosomes of two parent individuals. For each ``i``\\ th pair of corresponding chromosomes, the ``i``\\ th crossover function in ``args.crossparams`` is applied. The first child chromosome returned by each call is appended to the first child individual, and the second to the second child individual.

oneChildCrossover(args)
========================

.. function:: oneChildCrossover(args)

   :param args.p1: the first parent
   :type args.p1: instance of :class:`individual.Individual`
   :param args.p2: the second parent, with the same number of chromosomes as ``args.p1``
   :type args.p2: instance of :class:`individual.Individual`
   :param args.crossfuncs: a list of per-chromosome crossover functions, same length as ``args.p1``
   :type args.crossfuncs: list of functions
   :param args.crossparams: a list of parameters, one per entry in ``args.crossfuncs``
   :rtype: a single :class:`individual.Individual` child

Cross over all chromosomes of two parent individuals, producing one child. For each ``i``\\ th pair of corresponding chromosomes, ``args.crossfuncs[i]`` is applied and its result appended to the child individual.

.. warning::

    As currently written, :func:`oneChildCrossover` calls each per-chromosome crossover
    function as ``crossfunc(args.p1[i], args.p2[i], crossparams)`` -- three positional
    arguments. Every per-chromosome crossover function in this module (e.g.
    :func:`crossOnes`) instead follows the single-``args``-Namespace convention used
    everywhere else in this framework, and only accepts one parameter. Calling
    :func:`oneChildCrossover` with such a function will raise ``TypeError``. This is a
    real inconsistency in the current source, not a documentation gap -- see the
    top-level README's Known Issues.
