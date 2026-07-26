selection.py
************

getRouletteWheel(args)
========================

.. function:: getRouletteWheel(args)

   :param args.pop: the population for which a roulette wheel must be made
   :type args.pop: list of instances of :class:`individual.Individual`
   :param args.SCORES: a dictionary that maps instances of Individual to their fitnesses
   :type args.SCORES: dict {Individual: number}
   :rtype: list of 3-tuples ``(Individual, lowerBound, upperBound)``

Return a fitness-proportional roulette wheel.
A roulette wheel is a list of 3-tuples structured as follows:
``(indiv, low, high)`` where ``indiv`` is the individual that bets on the section of the roulette wheel between ``low`` and ``high``.

rouletteWheelSelect(args)
===========================

.. function:: rouletteWheelSelect(args)

   :param args.wheel: a roulette wheel, as returned by :func:`getRouletteWheel`
   :type args.wheel: a list of 3-tuples. Each tuple consists of the individual, the lower bound (float) of its section of the roulette wheel, and the upper bound (float) of its section of the roulette wheel.
   :param args.s: the random number on which the roulette ball lands on the roulette wheel. Optional -- if not supplied (or ``None``), a random float in ``[0, 1)`` is generated
   :type args.s: float, optional
   :rtype: single individual

Perform roulette wheel selection: a binary search over ``args.wheel`` for the individual whose section contains ``args.s``.

tournamentSelect(args)
========================

.. function:: tournamentSelect(args)

   :param args.population: the population to select from
   :type args.population: list of Individuals
   :param args.tournsize: the number of contestants in each tournament (``args.population`` must have at least this many individuals)
   :type args.tournsize: int
   :param args.numwinners: the number of winners kept from each tournament (must be at most ``args.tournsize``)
   :type args.numwinners: int
   :param args.numselect: the total number of individuals to select (must be a multiple of ``args.numwinners``, and at most ``args.tournsize``)
   :type args.numselect: int
   :param args.scorefunc: the function used to evaluate the fitness of individuals, to determine the winner(s) of a tournament
   :type args.scorefunc: function
   :param args.scoreparams: the parameters ``args.scorefunc`` requires, other than the individual itself (the individual being scored is set as ``args.scoreparams.individual`` for each call)
   :type args.scoreparams: argparse.Namespace
   :rtype: list of ``args.numselect`` individuals

Return a list of ``args.numselect`` individuals.
Each is selected by conducting tournaments of size ``args.tournsize``, drawn (with replacement across tournaments) from ``args.population``.
Each tournament keeps its fittest ``args.numwinners`` individuals, as determined by ``args.scorefunc``.
