population.py
*************

genPop(args)
=============

.. function:: genPop(args)

   :param args.popSize: the number of individuals in the population
   :type args.popSize: int
   :param args.chromGens: a list of ``(function, params)`` tuples. The ``i``\\ th tuple's function is responsible for generating the ``i``\\ th chromosome for each individual, called as ``function(params)``. The length of this list is exactly the number of chromosomes in each individual
   :type args.chromGens: list of (function, argparse.Namespace) tuples
   :rtype: list of unique individuals. Uniqueness is defined by ``Individual.__eq__``/``__hash__``

Return a population (list) of ``args.popSize`` unique individuals. Each individual has
``len(args.chromGens)`` chromosomes; chromosome ``i`` of every individual is generated
by calling ``args.chromGens[i][0](args.chromGens[i][1])``.

.. note::

    In order for :func:`genPop` to work, :class:`individual.Individual` must implement :func:`__hash__`. This is because :func:`genPop` uses a ``set`` internally before returning a list of individuals as the generated population.

genCharsChrom(args)
=====================

.. function:: genCharsChrom(args)

   :param args.numGenes: the length of the chromosome to generate
   :type args.numGenes: int
   :param args.bases: the alphabet to draw genes from (anything supporting ``__getitem__``/``__len__``, e.g. a string or list)
   :rtype: list of length ``args.numGenes``, each element drawn from ``args.bases``

Return a chromosome (list) of length ``args.numGenes``, each element of which is chosen (with replacement) from ``args.bases``. Used by the One-Max example.

genTour(args)
==============

.. function:: genTour(args)

   :param args.numCities: the number of cities in the tour
   :type args.numCities: int
   :rtype: list of ints -- a permutation of ``range(args.numCities)``

This is the chromosome generation function for the Traveling Salesman Problem. It returns a permutation of ``{0, 1, ..., args.numCities-1}``, representing a tour that the traveling salesman would take.

.. note::

    As described in the top-level README's Known Issues, the settings function that would wire this into a runnable TSP example is currently commented out in :doc:`settings.py`.
