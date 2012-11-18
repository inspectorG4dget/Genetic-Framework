Overview - How to use this Framework
*************************************
If you are making your own evolutionary algorithm, there are several files that you should edit

individual.py
==============
This file defines what an individual is (in a class). Generically, an :class:`individual` is simply an ordered collection of chromosomes. The original implementation treats each chromosome differently. Therefore, all the chromosomes of an individual are maintained in a ``list`` as opposed to a ``set``.

Also implemented in this file are methods to the ``individual`` class that help identify an individual, define its ``hash``, test its equality to another ``individual`` instance, etc

population.py
==============
This file contains the functions that define population generation.
The important function defined here is :func:`genPop`, which may be used as an interface to creating unique individuals.

.. function:: genPop(N, chromGenfuncs, chromGenParams)

   :param N: the number of individuals in the population
   :type N: int
   :param chromGenfuncs: a list of functions. The ith function is responsible for generating the ith chromosome for the individual. The length of this list is exactly the number of chromosomes in each individual
   :type chromGenfuncs: list of functions.
   :param chromGenfuncs: list of params for the functions in chromGenfuncs. The ith function in chromGenfuncs is called with the parameters held in the ith tuple of this list
   :type chromGenfuncs: list of tuples
   :rtype: list of unique individuals. Uniqueness is defined by ``Individual.__eq__``

chromGenfuncs
--------------
chromGenfuncs is a list of functions. The idea here is that each individual in the population is made up of C chromosomes. These C chromosomes are generated independently of each other for each individual in the initial population. Therefore, there must be exactly C functions listed in chromGenfuncs. The ``i`` th function in chromGenfuncs will be used to generate the ``i`` th chromosome of each individual

chromGenParams
---------------
chromGenParams is a list of tuples. There should be exactly as many tuples in this list, as there are functions in chromGenfuncs. To generate the ith chromosome for each individual in the population, the ith function in chromGenfuncs is called with the parameters in the ith tuple of chromGenParams as follows: ::

    chromGenfuncs[i](*chromGenParams[i])

Though that is the general idea behind how :func:`genPop` works, it actually performs this call in a for loop over a :func:`zip` of chromGenfuncs and chromGenParams

.. note::

    In order for :func:`genPop` to work, :class:`Individual` must implement :func:`__hash__`. This is because :func:`genPop` uses a ``set`` internally before returning a list of individuals as the generated population. As a result, a meaningful :func:`__hash__` must be implemented in :class:`Individual`.

fitness.py
==========
This file contains all selection functions for evaluating the fitness of any individual of the population. The main function in this file is called :func:`score`.

.. function:: score(p, scorefuncs, scorefuncparams, SCORES)

   :param p: the individual being evaluated
   :type p: instance of individual
   :param scorefuncs: a list of functions - one to evaluate each chromosome in the individual
   :type scorefuncs: list of functions
   :param scorefuncparams: a list of tuples containing the parameters for each of the functions in scorefuncs. Each function will be called by calling scorefuncs[i](p, *scorefuncparams[i])
   :type scorefunc params: list of tuples
   :param SCORES: a dict mapping instances of Individual to their fitness
   :type SCORES: dict {Individual : number}
   :rtype: number (the fitness of the individual)

.. note::

    if the individual being evaluated by this function (``p``) was not in ``SCORES`` before the function is executed, it will be inserted into ``SCORES`` by this function. Thus, ``SCORES`` is modified in-place by this function as required.


selection.py
=============
This file contains all selection functions for selecting individuals from a population for any purpose.

There are three important functions already implemented:

1. :func:`tournamentSelect`
2. :func:`rouletteWheelSelect`
3. :func:`getRouletteWheel`

:func:`tournamentSelect`
-------------------------

.. function:: tournamentSelect(pop, T, w, n, scorefunc, scoreparams)

   :param pop: the population to select from
   :type pop: list of Individuals
   :param T: the number of contestants in each tournament (must be smaller than len(pop))
   :type T: int
   :param w: the number of winners in each tournament (must be smaller than T)
   :type w: int
   :param n: the number of Individuals to be selected from the population by Tournament Selection (n%w should be 0)
   :type n: int
   :param scorefunc: the function used to evaluate the fitness of individuals, to determine the winner(s) of a tournament
   :type scorefunc: function
   :param scoreparams: the parameters that scorefunc requires, other than the individual itself. The individual is provided along with the unpacked list of params
   :type scoreparams: tuple
   :rtype: list of individuals


:func:`rouletteWheelSelect`
----------------------------

.. function:: rouletteWheelSelect(wheel, s=None)

   :param wheel: a roulette wheel
   :type wheel: a list of 3-tuples. Each tuple consists of the individual, the lower bound (float) of its section of the roulette wheel, and the upper bound (float) of its section of the roulette wheel.
   :param s: the random number on which the roulette ball lands on the roulette wheel. This is not provided when calling the function (though it may be if desired). Using this, a binary search is performed to find the Individual that bet on a section of the roulette wheel containing this number
   :type s: float
   :rtype: single individual


:func:`getRouletteWheel`
------------------------

.. function:: getRouletteWheel(pop, SCORES)

   :param pop: the population for which a roulette wheel must be made
   :type pop: list of instances of Individual
   :param SCORES: a dictionary that maps instances of Individual to their fitnesses
   :type SCORES: dict {Individual:number}
   :rtype: list of 3-tuples (Individual, lowerBound, UpperBound)

crossover.py
=============

All functions that have to do with crossing over chromosomes between individuals are defined here. There is no generic driver function here as crossovers are defined per GA.

mutation.py
============

All functions that have to do with mutating chromosomes between individuals are defined here. There is no generic driver function here as mutations are defined per GA

