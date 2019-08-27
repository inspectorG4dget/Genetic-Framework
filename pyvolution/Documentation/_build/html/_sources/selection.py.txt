selection.py
************
    
getRouletteWheel(pop, SCORES)
==============================
Return a fitness proportional roulette wheel.
A roulette wheel is a list of 3-tuples structured as follows:
(indiv, low, high) where indiv is the individual that bets on the section of the roulette wheel between low and high


rouletteWheelSelect(wheel, s=None)
===================================
Perform roulette wheel selection. A wheel is a fitness proportional roulette wheel as returned by the makeRouletteWheel function.
The parameter s is not required thought not disallowed at the time of calling by the evolutionary algorithm. If it is not supplied, it will be set as a random float between 0 and 1.
This function returns the individual that bet on the section of the roulette wheel that contains s

tournamentSelect(pop, T, w, n, scorefunc, scoreparams)
========================================================
Return a list of n indivuduals. 
Each of these individuals has been selected by conducting tournaments of size T.
Each tournament may have exactly w winners
Winners of the tournament are the fittest individuals in the tournament as determined by scorefunc
