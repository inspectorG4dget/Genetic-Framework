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
from random import choice as choose, sample

from individual import Individual
from pystitia import contracts


@contracts(
	preconditions=(
		lambda args: args.popSize>0,
		lambda args: isinstance(args.chromGens, list),
		lambda args: all(isinstance(t, tuple) for t in args.chromGens),
		lambda args: all(hasattr(f, '__call__') for f, _t in args.chromGens),
		lambda args: all(isinstance(t, argparse.Namespace) for _f, t in args.chromGens),
	),
	postconditions=(
		lambda: isinstance(__return__, list),
		lambda args: len(__return__) == args.popSize,
		lambda: all(__return__.count(indiv) == 1 for indiv in __return__),
		lambda args: __old__.args.chromGens == args.chromGens,
	)
)
def genPop(args):
	""" Return a population (list) of N unique individuals.
		Each individual has len(chromgGenFuncs) chromosomes.
		For each individual, chromosome_i is generated by calling chromGenFuncs_i(chromeGenParams_i)
	"""

	answer = set()
	while len(answer) < args.popSize:
		indiv = Individual([])
		for genfunc, genparams in args.chromGens:
			indiv.append(genfunc(genparams))
		answer.add(indiv)
	return list(answer)


@contracts(
	preconditions=(
		lambda args: isinstance(args.numGenes, int),
		lambda args: hasattr(args.bases, '__getitem__'),
		lambda args: hasattr(args.bases, '__len__'),
		lambda args: len(args.bases) > 0,
	),
	postconditions=(
		lambda args: __old__.args.numGenes == args.numGenes,
		lambda args: __old__.args.bases == args.bases,
		lambda args: len(__return__) == args.numGenes,
		lambda args: all(a in args.bases for a in __return__),
	)
)
def genCharsChrom(args):
	"""
	Return chromosome (list) of length numGenes, each of which is made up of the characters from args.bases.
	"""
	
	return [choose(args.bases) for _ in range(args.numGenes)]


@contracts(
	preconditions=(
		lambda args: isinstance(args.numCities, int),
	),
	postconditions=(
		lambda args: __old__.args.numCities == args.numCities,
		lambda: isinstance(__return__, list),
		lambda args: len(__return__) == args.numCities,
		lambda args: all(0<= c < args.numCities for c in __return__),
		lambda args: all(__return__.count(c)==1 for c in __return__),
	)
)
def genTour(args):
	return sample(range(args.numCities), args.numCities)
