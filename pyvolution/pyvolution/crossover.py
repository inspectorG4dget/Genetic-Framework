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

import argparse
import itertools

from individual import Individual
from random import randint, sample
from pystitia import contracts


@contracts(
	preconditions=(
		lambda args: isinstance(args.p1, list),
		lambda args: isinstance(args.p2, list),
	),
	postconditions=(
		lambda args: args.p1 == __old__.args.p1,
		lambda args: args.p2 == __old__.args.p2,
		lambda: isinstance(__return__, tuple),
		lambda: len(__return__)==2,
		lambda: all(isinstance(e, list) for e in __return__),
		# lambda args: all(child in args.p1 or child in args.p2 for child in __return__),
		lambda args: all(id(L) not in (id(args.p1), id(args.p2)) for L in __return__),
	)
)
def crossOnes(args): #p1, p2):
	""" Length preserving one-point crossover of chromosome at index chrom
		Tuple containing two new children is returned
	"""
	
	crosspoint = randint(0, len(args.p1)-1)
	child1 = args.p2[:crosspoint] + args.p1[crosspoint:]
	child2 = args.p1[:crosspoint] + args.p2[crosspoint:]
	
	return child1, child2


@contracts(
	preconditions=(
		lambda args: isinstance(args.p1, list),
		lambda args: isinstance(args.p2, list),
		lambda args: len(args.p1) == len(args.p2),
		lambda args: sorted(args.p1)==list(range(len(args.p1))),
		lambda args: sorted(args.p2)==list(range(len(args.p2))),
	),
	postconditions=(
		lambda args: args.p1 == __old__.args.p1,
		lambda args: args.p2 == __old__.args.p2,
		lambda: isinstance(__return__, list),
		lambda args: len(__return__) == len(args.p1),
		lambda args: id(__return__) not in (id(args.p1), id(args.p2)),
		lambda args: all(city in args.p1 and city in args.p2 for city in __return__),
		lambda: len(set(__return__)) == len(__return__),
	)
)
def injectionco(args): #p1, p2):

	answer = [None] * len(args.p1)
	a,b = sample(range(len(args.p1)), 2)
	if a > b: a,b = b,a
	ab = args.p1[a:b]
	answer[a:b] = ab
	remainder = [city for city in args.p2 if city not in ab][::-1]  # the reversing is an optimization to lose less time when popping
	for i in range(a):
		answer[i] = remainder.pop(-1)
	for i in range(b, len(answer)):
		answer[i] = remainder.pop(-1)
	
	return answer


# noinspection PyUnresolvedReferences,PyUnresolvedReferences,PyUnresolvedReferences,PyUnresolvedReferences,PyUnresolvedReferences
@contracts(
	preconditions=(
		# lambda args: isinstance(args.p1, Individual),
		# lambda args: isinstance(args.p2, Individual),
		# lambda args: len(args.p1)==len(args.p2),
		# lambda args: len(args.p1)==len(args.crossfuncs),
		lambda args: all(isinstance(p, tuple) for p in args.crossparams),
	),
	postconditions=(
		# lambda args: args.p1 == __old__.args.p1,
		# lambda args: args.p2 == __old__.args.p2,
		# lambda args: id(args.p1) == __id__.p1,
		# lambda args: id(args.p2) == __id__.p2,
 		lambda: len(__return__) == 2,
		lambda: all(isinstance(p, Individual) for p in __return__),
		# lambda args: all(len(p)==len(args.p1) for p in __return__),
		# lambda args: all(len(c)==len(c1) for p in __return__ for c,c1 in zip(p.chromosomes, args.p1.chromosomes)),
		# lambda args: all(len(c)==len(c1) for p in __return__ for c, c1 in zip(p.chromosomes, args.p2.chromosomes)),
	)
)
def twoChildCrossover(args): #p1,p2, crossfuncs, crossparams):
	"""
		Crossover all the chromosomes in the two individuals.
		The crossover function for each pair of  corresponding chromosomes is the the corresponding element in crossfuncs, 
		called with the corresponding tuple in crossparams.
		
		Note that it is assumed that each crossover function in crossfuncs returns two child chromosomes
	"""
	
	c1, c2 = [Individual([]) for _ in range(2)]
	for i, (crossfunc, crossparams) in enumerate(args.crossparams):
		params = argparse.Namespace()
		params.p1 = args.p1[i]
		params.p2 = args.p2[i]
		chrom1, chrom2 = crossfunc(params)
		c1.append(chrom1)
		c2.append(chrom2)
	
	return c1, c2


@contracts(
	preconditions=(
		lambda args: isinstance(args.p1, Individual),
		lambda args: isinstance(args.p2, Individual),
		lambda args: len(args.p1)==len(args.p2),
		lambda args: len(args.p1)==len(args.crossfuncs),
		lambda args: len(args.crossfuncs) == len(args.crossparams),
	),
	postconditions=(
		lambda args: args.p1 == __old__.args.p1,
		lambda args: args.p2 == __old__.args.p2,
		lambda args: id(args.p1) == __id__.args.p1,
		lambda args: id(args.p2) == __id__.args.p2,
		lambda: len(__return__)==1,
		lambda: isinstance(__return__, Individual),
		lambda args: len(__return__) == len(args.p1),
		lambda args: all(len(c)==len(args.p1[i]) for i,c in enumerate(__return__.chromosomes)),
		lambda args: all(len(c) == len(args.p2[i]) for i,c in enumerate(__return__.chromosomes)),
	)
)
def oneChildCrossover(args): #p1, p2, crossfuncs, crossparams):
	"""
		Crossover all the chromosomes in the two individuals.
		The crossover function for each pair of  corresponding chromosomes is the the corresponding element in crossfuncs, 
		called with the corresponding tuple in crossparams.
		
		Note that it is assumed that each crossover function in crossfuncs returns one child chromosome
	"""
	answer = Individual([])
	for i, crossfunc, crossparams in zip(itertools.count(), args.crossfuncs, args.crossparams):
		answer.append(crossfunc(args.p1[i], args.p2[i], crossparams))
	
	return answer
