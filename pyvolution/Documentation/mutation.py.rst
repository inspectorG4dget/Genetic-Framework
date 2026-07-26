mutation.py
************

Each function in this module returns a *new* :class:`individual.Individual` rather than mutating its input in place.

mutateSingleAllele(args)
==========================

.. function:: mutateSingleAllele(args)

   :param args.individual: the individual to mutate
   :type args.individual: instance of :class:`individual.Individual`
   :param args.chrom: which chromosome to mutate
   :type args.chrom: int
   :param args.chars: the alphabet to draw the replacement gene from
   :rtype: a new :class:`individual.Individual`

Return a new individual, which is the same as ``args.individual``, but with the ``args.chrom``\\ th chromosome changed as follows: select a random gene and change its value to something else from the choices in ``args.chars``.

swapmut(args)
==============

.. function:: swapmut(args)

   :param args.p: the individual to mutate
   :type args.p: instance of :class:`individual.Individual`
   :param args.chrom: which chromosome to mutate
   :type args.chrom: int
   :rtype: a new :class:`individual.Individual`

Get the ``args.chrom``\\ th chromosome of ``args.p``. Select two random genes in that chromosome and swap their positions.
Return a new individual that is the same as ``args.p``, but with the above change made to its ``args.chrom``\\ th chromosome.

revmut(args)
=============

.. function:: revmut(args)

   :param args.p: the individual to mutate
   :type args.p: instance of :class:`individual.Individual`
   :param args.chrom: which chromosome to mutate
   :type args.chrom: int
   :rtype: a new :class:`individual.Individual`

Get the ``args.chrom``\\ th chromosome of ``args.p``. Select two random points in that chromosome and reverse the order of the genes between them.
Return a new individual that is the same as ``args.p``, but with the above change made to its ``args.chrom``\\ th chromosome.

shufflemut(args)
=================

.. function:: shufflemut(args)

   :param args.p: the individual to mutate
   :type args.p: instance of :class:`individual.Individual`
   :param args.chrom: which chromosome to mutate
   :type args.chrom: int
   :rtype: a new :class:`individual.Individual`

Get the ``args.chrom``\\ th chromosome of ``args.p``. Shuffle that chromosome with ``random.shuffle``.
Return a new individual that is the same as ``args.p``, but with the above change made to its ``args.chrom``\\ th chromosome.

.. note::

    ``mutateSingleAllele`` names its individual parameter ``args.individual``, while
    ``swapmut``, ``revmut``, and ``shufflemut`` name theirs ``args.p``. This is an
    inconsistency in the current source's naming, not a documentation choice --
    functions in this module are not interchangeable drop-in replacements for each
    other's callers without adjusting the attribute name on ``args``.
