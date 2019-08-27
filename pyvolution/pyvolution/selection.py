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

import heapq
from random import sample, random as rand
from individual import Individual
from pystitia import contracts


@contracts(
	preconditions=(
		lambda args: isinstance(args.pop, list),
		lambda args: all(isinstance(p, Individual) for p in args.pop),
		lambda args: isinstance(args.SCORES, dict),
		lambda args: all(isinstance(i, Individual) for i in args.SCORES),
		lambda args: all(p in args.SCORES for p in args.pop),
	),
	postconditions=(
		lambda args: __old__.args.pop == args.pop,
		lambda: isinstance(__return__, list),
		lambda args: len(__return__) == len(args.pop),
		lambda: all(isinstance(t, tuple) for t in __return__),
		lambda: all(len(t)==3 for t in __return__),
		lambda: all(isinstance(t[0], Individual) for t in __return__),
		lambda args: all(t[0] in args.pop for t in __return__),
		lambda: all(isinstance(t[1], float) for t in __return__),
		lambda: all(isinstance(t[2], float) for t in __return__),
		lambda: all(t[1]<=t[2] for t in __return__)
	)
)
def getRouletteWheel(args): #pop, SCORES):
	""" Return a fitness proportional roulette wheel.
		A roulette wheel is a list of 3-tuples structured as follows:
		(indiv, low, high) where indiv is the individual that bets on the section of the roulette wheel between low and high
	"""
		
	answer = []
	top = 0.0
	total = sum(args.SCORES[p] for p in args.pop)
	for indiv in args.pop:
		segment = args.SCORES[indiv]/total
		answer.append((indiv, top, top+segment))
		top += segment
	return answer


@contracts(
	preconditions=(
		lambda args: isinstance(args.wheel, list),
		lambda args: all(isinstance(t, tuple) for t in args.wheel),
		lambda args: all(isinstance(t[0], Individual) for t in args.wheel),
		lambda args: all(isinstance(t[1], float) for t in args.wheel),
		lambda args: all(isinstance(t[2], float) for t in args.wheel),
		lambda args: all(t[1]<=t[2] for t in args.wheel),
		lambda args: (isinstance(args.s, float) ^ (args.s is None)) if getattr(args, 's', None) else True
	),
	postconditions=(
		lambda args: __old__.args.wheel == args.wheel,
		lambda: isinstance(__return__, Individual),
	)
)
def rouletteWheelSelect(args): #wheel, s=None):
	args.s = getattr(args, 's', None)  # fixing randomness
	if args.s is None: args.s = rand()

	start, end = 0, len(args.wheel)-1
	while start < end:
		mid = (start+end)//2
		indiv, low, high = args.wheel[mid]

		if low <= args.s <= high: return indiv
		if args.s < low: end = mid-1
		else: start = mid+1

	mid = (start + end) // 2
	indiv, low, high = args.wheel[mid]
	if low <= args.s <= high: return indiv

	raise ValueError("Roulette wheel did not find any individual")


@contracts(
	preconditions=(
		lambda args: isinstance(args.population, list),
		lambda args: all(isinstance(i, Individual) for i in args.pop),
		lambda args: isinstance(args.T, int),
		lambda args: isinstance(args.w, int),
		lambda args: isinstance(args.n, int),
		lambda args: args.w <= args.n,
		lambda args: args.n % args.w == 0,
		lambda args: args.w <= args.T,
		lambda args: len(args.pop) >= args.T,
		lambda args: args.T >= args.n,
		lambda args: isinstance(args.scoreparams, tuple),
	),
	postconditions=(
		lambda args: __old__.args.pop == args.pop,
		lambda args: __old__.args.T == args.T,
		lambda args: __old__.args.w == args.w,
		lambda args: __old__.args.n == args.n,
		lambda args: __old__.args.scorefunc == args.scorefunc,
		lambda args: __old__.args.scoreparams == args.scoreparams,
		lambda: isinstance(__return__, list),
		lambda args: len(__return__) == args.n,
	)
)
def tournamentSelect(args): #pop, T, w, n, scorefunc, scoreparams):
	""" Return a list of n indivuduals. 
		Each of these individuals has been selected by conducting tournaments of size T.
		Each tournament may have exactly w winners
		Winners of the tournament are the fittest individuals in the tournament as determined by scorefunc
		Prerequisites: n%w==0 and w<=T and pop>=T and pop>=n
	"""

	def scorer(p, func, args):
		args.individual = p
		return func(args)

	answer = []
	while len(answer) < args.numselect:
		answer.extend(heapq.nlargest(args.numwinners, sample(args.population, args.tournsize), key=lambda p: scorer(p, args.scorefunc, args.scoreparams)))
	return answer
