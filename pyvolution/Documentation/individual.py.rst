individual.py
*************

Define an individual to be used for evolution.

Class Variables
===============

``ID``
-------
An ``itertools.count()`` generator used to hand out a unique, trackable id to each ``Individual`` as it is constructed.

Instance variables
==================

``id``
------
A trackable identifier for the individual, taken from ``ID`` at construction time.

``chromosomes``
---------------
An ordered collection of the genetic material of this individual. Maintained as a list.

Methods
========

``__init__(self, chromosomes)``
--------------------------------
Construct an individual wrapping a copy of ``chromosomes`` (a list), and assign it the next ``id`` from ``ID``.

``__eq__(self, other)``
------------------------
Return True if all chromosomes of self and other are equal (and in the same order).
Else, return False.

``__hash__(self)``
-------------------
Return the hash of the tuple-of-tuples version of all chromosomes.

``__len__(self, chrom=None)``
-------------------------------
If ``chrom`` is ``None``, return the number of chromosomes ``self`` is made of. Otherwise, return the length of the ``chrom``\\ th chromosome.

``__iter__(self)``
--------------------
Return an iterator over ``self.chromosomes``.

``__getitem__(self, i)``
------------------------
Return the ``i``\\ th chromosome of ``self``.

``__setitem__(self, index, obj)``
---------------------------------
Set ``obj`` as the ``index``\\ th chromosome of ``self``.

``__contains__(self, chromosome)``
----------------------------------
Return True if ``chromosome`` is a member of ``self.chromosomes``.
Else return False.

``__repr__(self)``
-------------------
Return a string representation showing all of ``self``'s chromosomes.

``__str__(self)``
-------------------
Return ``self.id`` as a string.

``append(self, chrom)``
-----------------------
Append ``chrom`` to ``self.chromosomes``.

``count(self, sub, chrom)``
-----------------------------
Return the number of occurrences of ``sub`` in the ``chrom``\\ th chromosome of ``self``.
