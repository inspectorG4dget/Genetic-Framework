Contracts
**********

Contracts are used to check the pre and post conditions of functions to make sure that the evolutionary algorithm remains constrained within the solution space.

All contracts used by all functions are listed here. It is highly recommended that similar functions that are implemented in the future implement similar contracts. This will be explained further as each contract is explaioned.

GA.py
=====

The main GA driver has the following contracts. It is highly recommended that any GA implemented to maximize the fitness score should implement these contracts.

The main GA runner
------------------

Preconditions
++++++++++++++
1. ``kwargs`` should be supplied
2. ``kwargs`` is a dict mapping argument names (strings) to argument values
3. The maximum number of generations allowed is greater than 0

Postconditions
++++++++++++++
1. ``kwargs`` should not be changed
2. At least one of the following two conditions must hold
	a. the fitness of the fittest individual (being returned) is at least ``targetscore``
	b. the current generation count is equal to the maximum number of generations allowed
3. the maximum number of generations allowed is greater than 0

Individual.py
=============

The following contracts must be followed for any implementation of the ``Individual`` class


``Individual.__hash__(self, other)``
------------------------------------

Preconditions
++++++++++++++
None

Postconditions
++++++++++++++
1. an ``int`` should be returned
2. ``self`` should not be changed

In addition to these, the current implementation has the following methods implemented:

``Individual.__eq__(self, other)``
----------------------------------

Preconditions
++++++++++++++
1. ``other`` should be an instance of :class:`Individual`

Postconditions
++++++++++++++
1. ``other`` should not be changed
2. ``self`` should not be changed

``Individual.__len__(self)``
--------------------------------

Preconditions
++++++++++++++
None

Postconditions
++++++++++++++
1. ``self`` should not be changed

``Individual.__setitem__(self, index, obj)``
---------------------------------------------

Preconditions
++++++++++++++
1. Exactly one of the following two conditions must be satisfied:
	a. 0 <= ``index`` <= len(self.chromosomes)
	b. len(self.chromosomes)*-1 >= index >= -1

Postconditions
++++++++++++++
1. The object at ``self.chromosomes[index]`` should be ``obj``

``Individual.__contains__(self, chromosome)``
----------------------------------------------

Preconditions
++++++++++++++
None

Postconditions
++++++++++++++
1. ``self`` should not be changed
2. ``chromosome`` should not be changed

``Individual.__repr__(self)``
--------------------------------

Preconditions
++++++++++++++
None

Postconditions
++++++++++++++
1. ``self`` should not be changed

``Individual.append(self, chrom)``
-----------------------------------

Preconditions
++++++++++++++
None

Postconditions
++++++++++++++
1. The length of ``self.chromosomes`` should be increased by exactly 1
2. The last chromosome in ``self.chromosomes`` should be ``chrom``

``Individual.count(self, sub, chrom)``
---------------------------------------

Preconditions
++++++++++++++
None

Postconditions
++++++++++++++
1. ``self`` should not be changed


population.py
=============

The following contracts are applied to the functions in population.py

``genPop(N, chromGenfuncs, chromGenParams)``
---------------------------------------------

Preconditions
++++++++++++++
1. N >= 0
2. ``chromGenfuncs`` is a list
3. Every entry in ``chromGenfuncs`` is a function
4. ``chromGenParamss`` is a list
5. The lengths of ``chromGenfuncs`` and ``chromGenParams`` are equal

Postconditions
++++++++++++++
1. The inputs are unchanged
2. Function returns a list
3. The length of the returned list is ``N``
4. The returned list contains exactly 1 of each item i.e. no two items in the returned list are equal


``genCharsChrom(l, chars)``
----------------------------

Preconditions
++++++++++++++
1. ``l`` is an integer
2. ``chars`` is an instance of some class that implements ``__getitem__``
3. ``chars`` is an instance of some class that implements ``__len__``
4. ``len(chars)`` is greater than 0

Postconditions
++++++++++++++
1. The inputs are unchanged
2. Function returns a list
3. The length of the returned list is ``l``
4. Every element in the returned list exists in ``chars``

``genTour(numCities)``
----------------------------

Preconditions
++++++++++++++
1. ``numCities`` is an integer

Postconditions
++++++++++++++
1. The inputs are unchanged
2. Function returns a list
3. The length of the returned list is ``numCities``
4. Every element in the returned list exists exactly once in the returned list.

score.py
========

``score(p, scorefuncs, scorefuncparams, SCORES)``
-------------------------------------------------

Preconditions
++++++++++++++
1. ``p`` is an instance of :class:`Individual`
2. ``scorefuncs`` is a list of functions
3. ``scorefuncparams`` is a list of tuples
4. The lengths of ``scorefuncs`` and ``scorefuncparams`` are equal
5. ``SCORES`` is a dictionary

Postconditions
++++++++++++++
1. The inputs are unchanged
2. ``p`` is in ``SCORES``
3. Exactly one of the following two conditions are met:
	a. ``p`` was in ``SCORES`` before this function was called and the number of entries in ``SCORES`` has not changed
	b. ``p`` was not in ``SCORES`` before this function was called and the number of entries in ``SCORES`` has increased by exactly 1

``scoreOnes(p)``
----------------

Preconditions
++++++++++++++
1. ``p`` is list
2. All elements in ``p`` are strings of length exactly 1
3. All elements in ``p`` are either '0' or '1'

Postconditions
++++++++++++++
1. ``p`` is unchaged
2. An integer is returned
3. The value returned is at least 0

scoreTSP(tour, DIST)
--------------------
		post:
			isinstance(__return__, float)
		post[tour, DIST]:
			__old__.tour == tour
			__old__.DIST == DIST

Preconditions
+++++++++++++
1. ``tour`` is a list
2. ``DIST`` is a dictionary
3. All elements in ``tour`` are integers
4. All keys in ``DIST`` are integers
5. All values in ``DIST`` are dictionaries
6. Every key in every value of ``DIST`` is an integer
7. Every value in every value of ``DIST`` is a float

Loop Invariant
+++++++++++++++
1. ``answer`` (the value to be returned is at most 0 and monotonously decreases

Postconditions
+++++++++++++++
1. The inputs are unchanged
2. The function returns a float

getRouletteWheel(pop, SCORES)
------------------------------

Preconditions
+++++++++++++
1. ``pop`` is a list of instances of :class:`Individual`
2. ``SCORES`` is a dictionary
3. Every element in ``pop`` is a key in ``SCORES``

Postconditions
++++++++++++++
1. The inputs are unchanged
2. A list of 3-tuples of type (Individual, float, float) is returned
3. The length of the returned list is equal to the length of ``pop``
4. The first element of every tuple in the returned list exists in ``pop``
5. The second float is smaller than the third float in every tuple in the returned list

rouletteWheelSelect(wheel, s=None)
-----------------------------------

Preconditions
+++++++++++++
1. ``wheel`` is a list of 3-tuples which satisfy all the following conditions
	a. The first element is an instance of :class:`Individual`
	b. The last two elements are floats
	c. The first float is smaller than the second
2. Exactly one of the following two conditions are met:
	a. ``s`` is a float
	b. ``s`` is None

Postconditions:
+++++++++++++++
1. The inputs are unchanged
2. An instance of :class:`Individual` is returned

tournamentSelect(pop, T, w, n, scorefunc, scoreparams)
------------------------------------------------------

Preconditions
++++++++++++++
1. ``pop`` is a list of instances of :class:`Individual`
2. ``T`` is an integer
3. ``w`` is an integer
4. ``n`` is an integer
5. ``w`` is at most ``n``
6. ``n%w`` is exactly 0
7. ``n`` is at most ``T``
8. ``scoreparams`` is a tuple

Postconditions
++++++++++++++
1. The inputs are unchanged
2. A list of ``n`` instances of :class:`Individual` is returned

crossover.py
=============

The following contracts are implemented for the crossover functions.

crossOnes(p1, p2, chrom)
------------------------

Preconditions
+++++++++++++
1. ``p1`` and ``p2`` are instances of :class:`list`

Postconditions
+++++++++++++++
1. The inputs are unchaged
2. A tuple of two instances of :class:`list` is returned
3. Each list in the return tuple satisfies the following conditions:
	a. each element in the list exists in either ``p1`` or ``p2`` or both.

injectionco(p1, p2, chrom)
---------------------------

Preconditions
++++++++++++++
1. ``p1`` and ``p2`` are instances of :class:`list`
2. The length of `p1` is exactly equal to the length of ``p2``
3. ``p1`` is a permutation of [0… ``len(p1)-1``]
4. ``p2`` is a permutation of [0… ``len(p2)-1``]

Postconditions
++++++++++++++
1. The inputs are unchaged
2. A new object is returned of type :class:`list`
3. The length of the returned list is exactly equal to the length of ``p1`` (and therefore of ``p2`` as well)
4. The function returns a permutation i.e. all elements in the returned list occur exactly once

twoChildCrossover(p1,p2, crossfuncs, crossparams)
--------------------------------------------------

Preconditions
++++++++++++++
1. ``p1`` and ``p2`` are instances of :class:`Individual`
2. ``p1`` and ``p2`` are of exactly equal length
3. The number of elements in ``crossfuncs`` is exactly equal to the length of ``p1`` (and therefore of ``p2``)
4. The number of elements in ``crossfuncs`` is exactly equal to the number of elements in ``crossparams``
5. Every element in ``crossparams`` is a tuple

Postconditions
++++++++++++++
1. The inputs are unchanged
2. A tuple of two elements of type :class:`Individual` is returned
3. Each of the returned children has the same number of chromosomes as the parents
4. Each chromosome in each of the children has the same length as the corresponding chromosome of both parents

oneChildCrossover(p1,p2, crossfuncs, crossparams)
--------------------------------------------------

Preconditions
++++++++++++++
1. ``p1`` and ``p2`` are instances of :class:`Individual`
2. ``p1`` and ``p2`` are of exactly equal length
3. The number of elements in ``crossfuncs`` is exactly equal to the length of ``p1`` (and therefore of ``p2``)
4. The number of elements in ``crossfuncs`` is exactly equal to the number of elements in ``crossparams``
5. Every element in ``crossparams`` is a tuple

Postconditions
++++++++++++++
1. The inputs are unchanged
2. A tuple of one element of type :class:`Individual` is returned
3. The returned child has the same number of chromosomes as the parents
4. Each chromosome in the child has the same length as the corresponding chromosome of both parents

muatation.py
============

mutateSingleAllele(p, chrom, chars)
-----------------------------------

Preconditions
+++++++++++++
1. ``p`` is an instance of :class:`Individual`
2. ``chrom`` is an integer
3. The value of each gene in the ``chrom`` th chromosome of ``p`` exists in ``chars``
4. Exactly one of the following two conditions must be satisfied:
	a. 0 <= ``index`` <= len(self.chromosomes)
	b. len(self.chromosomes)*-1 >= index >= -1

Postconditions
++++++++++++++
1. The inputs are unchanged
2. A new instance of :class:`Individual` is returned
3. The ``chrom`` th chromosome of the returned individual is not equal to the ``chrom`` th chromosome of ``p``
4. All other chromosomes of the returned individual are exactly the same as the corresponding chromosome of ``p``

swapmut(p, chrom)
------------------

Preconditions
+++++++++++++
1. ``p`` is an instance of :class:`Individual`
2. ``chrom`` is an integer
3. Exactly one of the following two conditions are satisfied:
	a. 0 <= ``chrom`` <= ``len(p.chromosomes)``
	b. ``len(self.chromosomes)*-1`` >= ``index`` >= -1

Postconditions
++++++++++++++
1. The inputs are unchaged
2. An instance of :class:`Individual` is returned
3. All values in the ``chrom`` th chromosome of ``p`` are present in the ``chrom`` th chromosome of the output individual
4. The ``chrom`` th chromosomes of the output individual and ``p`` are not equal
5. There are exactly two genes in the ``chrom`` th chromome of ``p`` and the returned individual, whose values differ

revmut(p, chrom)
-----------------

Preconditions
+++++++++++++
1. ``p`` is an instance of :class:`Individual`
2. ``chrom`` is an integer
3. Exactly one of the following two conditions are satisfied:
	a. 0 <= ``chrom`` <= ``len(p.chromosomes)``
	b. ``len(self.chromosomes)*-1`` >= ``index`` >= -1

Postconditions
++++++++++++++
1. The inputs are unchaged
2. An instance of :class:`Individual` is returned
3. All values in the ``chrom`` th chromosome of ``p`` are present in the ```chrom`` th chromosome of the output individual
4. The ``chrom`` th chromosomes of the output individual and ``p`` are not equal

shufflemut(p, chrom)
--------------------

		post[p, chrom]:
			__old__.p == p
			__old__.chrom == chrom
			isinstance(__return__, Individual)
			__return__.chromosomes[chrom] != p.chromosomes[chrom]
			forall(p.chromosomes[chrom], lambda e: e in __return__.chromosomes[chrom])
			forall(__return__.chromosomes[chrom], lambda e: e in p.chromosomes[chrom])

Preconditions
+++++++++++++
1. ``p`` is an instance of :class:`Individual`
2. ``chrom`` is an integer
3. Exactly one of the following two conditions are satisfied:
	a. 0 <= ``chrom`` <= ``len(p.chromosomes)``
	b. ``len(self.chromosomes)*-1`` >= ``index`` >= -1

Postconditions
++++++++++++++
1. The inputs are unchaged
2. An instance of :class:`Individual` is returned
3. All values in the ``chrom`` th chromosome of ``p`` are present in the ```chrom`` th chromosome of the output individual
4. The ``chrom`` th chromosomes of the output individual and ``p`` are not equal
5. The length of the ``chrom`` th chromosome of the returned individual is exactly equal to the length of the ``chrom`` th chromosome of ``p``
