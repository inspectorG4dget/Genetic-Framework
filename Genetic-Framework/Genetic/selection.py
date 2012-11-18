'''
Copyright 2012 Ashwin Panchapakesan

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''

from random import sample, random as rand
from Genetic.individual import Individual #@UnusedImport # used only for contract checking

def getRouletteWheel(pop, SCORES):
	""" Return a fitness proportional roulette wheel.
		A roulette wheel is a list of 3-tuples structured as follows:
		(indiv, low, high) where indiv is the individual that bets on the section of the roulette wheel between low and high
	
		pre:
			isinstance(pop, list)
			forall(pop, lambda i: isinstance(i, Individual))
			isinstance(SCORES, dict)
			forall(SCORES, lambda i: isinstance(i, Individual))
			forall(pop, lambda i: i in SCORES)
		
		post[pop, SCORES]:
			__old__.pop == pop
			isinstance(__return__, list)
			len(__return__) == len(pop)
			forall(__return__, lambda t: isinstance(t, tuple))
			forall(__return__, lambda t: len(t)==3)
			forall(__return__, lambda t: isinstance(t[0], Individual))
			forall(__return__, lambda t: t[0] in pop)
			forall(__return__, lambda t: isinstance(t[1], float))
			forall(__return__, lambda t: isinstance(t[2], float))
			forall(__return__, lambda t: t[1] <= t[2])
			
	"""
		
	answer = []
	top = 0.0
	total = float(sum(SCORES[p] for p in pop))
	for indiv in pop:
		answer.append( (indiv, top, top+(SCORES[indiv]/total)) )
		top += SCORES[indiv]/total
	return answer

def rouletteWheelSelect(wheel, s=None):
	"""
		pre:
			isinstance(wheel, list)
			forall(wheel, lambda t: isinstance(t, tuple))
			forall(wheel, lambda t: len(t)==3)
			forall(wheel, lambda t: isinstance(t[0], Individual))
			forall(wheel, lambda t: isinstance(t[1], float))
			forall(wheel, lambda t: isinstance(t[2], float))
			forall(wheel, lambda t: t[1] <= t[2])
			isinstance(s, float) ^ isinstance(s, None.__class__)
		
		post[wheel]:
			__old__.wheel == wheel
			isinstance(__return__, Individual)
			
	"""
	
	if s is None:
		s = rand()

	indiv,low, high = wheel[len(wheel)/2]
	if low <= s <= high:
		return indiv
	elif high <= s:
		return rouletteWheelSelect(wheel[len(wheel)/2:], s)
	elif low >= s:
		return rouletteWheelSelect(wheel[:len(wheel)/2], s)

def tournamentSelect(pop, T, w, n, scorefunc, scoreparams):
	""" Return a list of n indivuduals. 
		Each of these individuals has been selected by conducting tournaments of size T.
		Each tournament may have exactly w winners
		Winners of the tournament are the fittest individuals in the tournament as determined by scorefunc
		Prerequisites: n%w==0 and w<=T and pop>=T and pop>=n
		
		pre:
			isinstance(pop, list)
			forall(pop, lambda i: isinstance(i, Individual))
			isinstance(T, int)
			isinstance(w, int)
			isinstance(n, int)
			w <= n
			n%w == 0
			w <= T
			len(pop) >= T
			T >= n
			isinstance(scoreparams, tuple)
		
		post[pop, T, w, n, scorefunc, scoreparams]:
			__old__.pop == pop
			__old__.T == T
			__old__.w == w
			__old__.n == n
			__old__.scorefunc == scorefunc
			__old__.scoreparams == scoreparams
		
		post:
			isinstance(__return__, list)
			len(__return__) == n
			forall(__return__, lambda i: isinstance(i, Individual))
		"""
	
	answer = []
	while len(answer) < n:
		answer.extend(sorted(sample(pop, T), key=lambda p: scorefunc(p, *scoreparams), reverse=True)[:w])
	return answer
