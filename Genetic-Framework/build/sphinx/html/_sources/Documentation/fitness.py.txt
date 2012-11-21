fitness.py
***********

score(p, scorefuncs, scorefuncparams, SCORES)
=============================================

Return the sum of the fitness of each chromosome of individual p and store the result in SCORES (mapped under p)
The score of the chromosome_i is determined by the call scorefunc[i](p.chromosomes[i], *scorefuncparams[i])

scoreOnes(p)
=============
Return the number of '1's in the chromosome p

scoreTSP(tour, DIST)
=====================
Return the total distance of ``tour``, a list of ints, representing a tour (each int is a city ID).
``DIST`` is a dictionary: {source_city_id : {destination_city_id : distance between source_city and desitantion_city} }