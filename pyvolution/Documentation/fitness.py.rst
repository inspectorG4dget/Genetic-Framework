fitness.py
***********

score(args)
============

.. function:: score(args)

   :param args.individual: the individual being evaluated
   :type args.individual: instance of :class:`individual.Individual`
   :param args.scorefuncs: a list of ``(function, params)`` tuples -- one per chromosome. The ``i``\\ th function is called as ``function(params)``, where ``params.individual`` is set to ``args.individual`` and ``params.chrom`` is set to ``i`` for the duration of the call
   :type args.scorefuncs: list of (function, argparse.Namespace) tuples
   :param args.SCORES: a dict mapping instances of :class:`individual.Individual` to their fitness
   :type args.SCORES: dict {Individual: number}
   :rtype: number (the fitness of ``args.individual``)

Return the sum of the fitness of each chromosome of ``args.individual``, and cache the result in ``args.SCORES`` (keyed by ``args.individual``).

.. note::

    If ``args.individual`` was not already a key in ``args.SCORES`` before this function ran, it is inserted. ``args.SCORES`` is therefore modified in place as needed.

scoreOnes(args)
================

.. function:: scoreOnes(args)

   :param args.individual: the individual being scored
   :type args.individual: instance of :class:`individual.Individual`
   :param args.chrom: which chromosome of ``args.individual`` to score
   :type args.chrom: int
   :rtype: int, at least 0

Return the number of ``'1'`` genes in the ``args.chrom``\\ th chromosome of ``args.individual``. This is the fitness function for the One-Max problem.

scoreTSP(args)
===============

.. function:: scoreTSP(args)

   :param args.tour: a tour -- a list of ints, each an index into ``args.DIST``
   :type args.tour: list of int
   :param args.DIST: ``{source_city_id: {destination_city_id: distance}}``
   :type args.DIST: dict
   :rtype: float (the negative of the total tour distance)

Return the negative of the total distance of ``args.tour`` (negative so that, consistent with every other fitness function in this framework, a higher score is better).

.. note::

    Traveling Salesman Problem (TSP) support is partial/removed (see the top-level
    README's Known Issues and the note in :doc:`settings.py`). ``scoreTSP`` also reads
    ``args.tour``/``args.DIST`` directly, rather than ``args.individual``/``args.chrom``
    the way :func:`scoreOnes` does -- so unlike ``scoreOnes``, it cannot be dropped into
    :func:`score`'s ``args.scorefuncs`` list without an adapter that populates
    ``args.tour`` from ``args.individual[args.chrom]``.
