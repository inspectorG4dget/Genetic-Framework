mutaion.py
************

mutateSingleAllele(p, chrom, chars)
====================================
Return a new individual, which is the same as ``p``, but with the ``chrom`` th chromosome changed as follows:
Select a random gene and change its value to something from the choices in ``chars``

``swapmut(p, chrom)``
=====================
Get the ``chrom`` th individual in p. Select two random elements in that chromosome and swap their positions in that chromosome
Return a new individual that is the same as ``p``, but with the above change made to its ``chrom`` th chromosome

``revmut(p, chrom)``
=====================
Get the ``chrom`` th individual in p. Select two random elements in that chromosome and reverse the order of genes between those two elements in that chromosome
Return a new individual that is the same as ``p``, but with the above change made to its ``chrom`` th chromosome

``shufflemut(p, chrom)``
=========================
Get the ``chrom`` th individual in p. Shuffle that chromosome with ``random.shuffle``
Return a new individual that is the same as ``p``, but with the above change made to its ``chrom`` th chromosome