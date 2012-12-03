crossover.py
************

crossOnes(p1, p2)
========================

Take two chromosomes (``p1`` and ``p2`` ).
Cross them over.
Return two new child chromosomes

injectionco(p1, p2, chrom)
==========================

Take two chromosomes ``p1`` and ``p2``.
Crossover them over as follows:

1. Select distinct points A < B between 0 and ``len(p1.chromosomes[chrom])``
2. Make an empty child chromosome of length ``len(p1.chromosomes[chrom])``
3. Copy over the genes of ``p1`` from A to (but not including) B into the corresponding genes of the child
4. Fill in the rest of the genes of the child with the genes from ``p2``, in the order in which they appear in ``p2``, making sure not to include alleles that already exist in the child

Return the child chromosome

twoChildCrossover(p1,p2, crossfuncs, crossparams)
=================================================

Take two parents, ``p1`` and ``p2``.
Assume that ``crossfuncs`` and ``crossparams`` are of equal length
Make two empty individuals to be returned as the answer
For each ``i``th pair of corresponding chromosomes in ``p1`` and ``p2``, cross them over with the corresponding ``i``th function in ``crossfuncs`` (and pass in the ``i``th tuple of parameters from ``crossparams``)
It is assumed that each function in ``crossparams`` returns two child chromosomes.
When crossover on each pair of chromosomes is complete, add the first child chromosome to the first child individual to be returned and the second child chromosome to the second child individual to be returned.
When all crossover operations are complete, return the two child individuals as the product of crossing over ``p1`` and ``p2``.

oneChildCrossover(p1, p2, crossfuncs, crossparams)
==================================================

Take two parents, ``p1`` and ``p2``.
Assume that ``crossfuncs`` and ``crossparams`` are of equal length
Make an empty individual to be returned as the answer
For each ``i``th pair of corresponding chromosomes in ``p1`` and ``p2``, cross them over with the corresponding ``i``th function in ``crossfuncs`` (and pass in the ``i``th tuple of parameters from ``crossparams``)
It is assumed that each function in ``crossparams`` returns one child chromosome
When crossover on each pair of chromosomes is complete, add the child chromosome to the child individual to be returned
When all crossover operations are complete, return the child individual as the product of crossing over ``p1`` and ``p2``.